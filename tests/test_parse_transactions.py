import zipfile
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.parse_transactions import parse_csv_with_pandas, parse_xlsx_with_pandas

############################################################################
# тесты для parse_csv_with_pandas(path)

#####
# 1с


def test_parse_csv_file_not_found():
    """тест когда файл не существует"""
    #  передаваемый путь к файлу
    fake_path = "fake_transactions.csv"
    # метод is_file возвратит False
    with patch.object(Path, "is_file", return_value=False):
        result = parse_csv_with_pandas(fake_path)
    # проверка что вернулася строка 'file not found'
    assert result == "file not found"


#####
# 2с


def test_parse_csv_with_valid_data():
    """тест успешного парсинга корректных данных"""
    fake_path = "valid_transactions.csv"
    # данные которые вернул бы pd.read_csv
    mock_data = {
        "id": [1, 2],
        "state": ["EXECUTED", "CANCELED"],
        "date": ["2026-10-27", "2026-10-26"],
        "amount": [100.5, 200.0],
        "currency_name": ["руб.", "USD"],
        "currency_code": ["RUB", "USD"],
        "description": ["Перевод организации", "Перевод частному лицу"],
        "from": ["Visa 1234", "MasterCard 5678"],
        "to": ["Счет 9876", "Счет 5432"],
    }
    mock_df = pd.DataFrame(mock_data)
    # патчим Path.is_file -возвращаем True и pd.read_csv -возвращаем наш DataFrame
    with patch.object(Path, "is_file", return_value=True), patch("pandas.read_csv", return_value=mock_df) as mock_read:
        result = parse_csv_with_pandas(fake_path)
        # проверка что pandas вызывался с правильными аргументами один раз
        mock_read.assert_called_once_with(Path(fake_path), sep=";")
    # проверка структуры списка и данных первого словаря
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["operationAmount"]["amount"] == 100.5
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"
    assert result[0]["from"] == "Visa 1234"


#####
# 3с


def test_parse_csv_with_nan_and_missing_values():
    """тест замены NaN и отсутствующих значений на None"""
    fake_path = "nan_transactions.csv"
    # данные где часть полей содержит None/NaN
    mock_data = {
        "id": [None],
        "state": [None],
        "date": [None],
        "amount": [None],
        "currency_name": [None],
        "currency_code": [None],
        "description": [None],
        "from": [None],
        "to": [None],
    }
    mock_df = pd.DataFrame(mock_data)
    with patch.object(Path, "is_file", return_value=True), patch("pandas.read_csv", return_value=mock_df):
        result = parse_csv_with_pandas(fake_path)
    assert len(result) == 1
    item = result[0]
    # проверяем логику замен
    assert item["id"] is None
    assert item["state"] is None
    assert item["operationAmount"]["amount"] is None
    assert item["operationAmount"]["currency"]["name"] is None
    assert item["from"] is None


####
# 4с


def test_parse_csv_corrupted_structure():
    """тест когда csv-файл поврежден (ошибка парсинга pandas)"""
    fake_path = "corrupted.csv"
    # Патчим is_file (файл есть), но read_csv вызывает ParserError
    with (
        patch.object(Path, "is_file", return_value=True),
        patch("pandas.read_csv", side_effect=pd.errors.ParserError("Error tokenizing data. C error: ...")),
    ):
        result = parse_csv_with_pandas(fake_path)
    assert result == "error csv format"


####
# 5с


def test_parse_csv_empty_file():
    """тест когда файл существует но он абсолютно пустой"""
    fake_path = "empty.csv"
    # read_csv выбрасывает EmptyDataError, если в файле нет данных/заголовков
    with (
        patch.object(Path, "is_file", return_value=True),
        patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError("No columns to parse from file")),
    ):
        result = parse_csv_with_pandas(fake_path)
    assert result == "file is empty"


####
# 6с


def test_parse_csv_missing_required_columns():
    """тест когда CSV валидный но в нем нет нужных колонок например, 'id'"""
    fake_path = "missing_columns.csv"
    # DataFrame в котором вообще нет колонки 'id' и 'amount'
    wrong_mock_data = {
        "state": ["EXECUTED"],
        "date": ["2026-10-27"],
        # колонка 'id' отсутствует
    }
    wrong_df = pd.DataFrame(wrong_mock_data)
    with patch.object(Path, "is_file", return_value=True), patch("pandas.read_csv", return_value=wrong_df):
        result = parse_csv_with_pandas(fake_path)
    assert result == "error csv data format"


############################################################################
# тесты для parse_xlsx_with_pandas(path)

#####
# 1x


def test_parse_xlsx_file_not_found():
    """тест когда файл не существует"""
    #  передаваемый путь к файлу
    fake_path = "fake_transactions.xlsx"
    # метод is_file возвратит False
    with patch.object(Path, "is_file", return_value=False):
        result = parse_xlsx_with_pandas(fake_path)
    # проверка что вернулся пустой список
    assert result == "file not found"


#####
# 2x


def test_parse_xlsx_with_valid_data():
    """тест успешного парсинга корректных данных"""
    fake_path = "valid_transactions.xlsx"
    # данные которые вернул бы pd.read_excel
    mock_data = {
        "id": [1, 2],
        "state": ["EXECUTED", "CANCELED"],
        "date": ["2026-10-27", "2026-10-26"],
        "amount": [100.5, 200.0],
        "currency_name": ["руб.", "USD"],
        "currency_code": ["RUB", "USD"],
        "description": ["Перевод организации", "Перевод частному лицу"],
        "from": ["Visa 1234", "MasterCard 5678"],
        "to": ["Счет 9876", "Счет 5432"],
    }
    mock_df = pd.DataFrame(mock_data)
    # Патчим Path.is_file -возвращаем True и pd.read_excel возвращаем наш DataFrame
    with (
        patch.object(Path, "is_file", return_value=True),
        patch("pandas.read_excel", return_value=mock_df) as mock_read,
    ):
        result = parse_xlsx_with_pandas(fake_path)
        # проверяем что pandas вызывался с правильными аргументами один раз
        mock_read.assert_called_once_with(Path(fake_path))
    # проверяем структуру и данные первого элемента
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["operationAmount"]["amount"] == 100.5
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"
    assert result[0]["from"] == "Visa 1234"


#####
# 3x


def test_parse_xlsx_with_nan_and_missing_values():
    """тест замены NaN и отсутствующих значений на None и пустые строки"""
    fake_path = "nan_transactions.xlsx"
    # данные где часть полей содержит None/NaN
    mock_data = {
        "id": [None],
        "state": [None],
        "date": [None],
        "amount": [None],
        "currency_name": [None],
        "currency_code": [None],
        "description": [None],
        "from": [None],
        "to": [None],
    }
    mock_df = pd.DataFrame(mock_data)
    with patch.object(Path, "is_file", return_value=True), patch("pandas.read_excel", return_value=mock_df):
        result = parse_xlsx_with_pandas(fake_path)
    assert len(result) == 1
    item = result[0]
    # проверяем результат
    assert item["id"] is None
    assert item["state"] is None
    assert item["operationAmount"]["amount"] is None
    assert item["operationAmount"]["currency"]["name"] is None
    assert item["from"] is None


#####
# 4x


def test_parse_xlsx_corrupted_structure():
    """тест когда excel-файл поврежден (ошибка парсинга pandas)"""
    fake_path = "corrupted.xlsx"
    # патчим is_file -файл есть но read_excel вызывает BadZipFile
    with (
        patch.object(Path, "is_file", return_value=True),
        patch("pandas.read_excel", side_effect=zipfile.BadZipFile("File is not a zip file")),
    ):
        result = parse_xlsx_with_pandas(fake_path)
    assert result == "error excel format"


#####
# 5x


def test_parse_xlsx_empty_file():
    """тест когда файл существует но он абсолютно пустой"""
    fake_path = "empty.xlsx"
    # read_csv выбрасывает EmptyDataError если в файле нет данных/заголовков
    with (
        patch.object(Path, "is_file", return_value=True),
        patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError("No columns to parse from file")),
    ):
        result = parse_xlsx_with_pandas(fake_path)
    assert result == "file is empty"


#####
# 6x


def test_parse_xlsx_missing_required_columns():
    """тест когда EXCEL валидный но в нем нет нужных колонок (например, 'id')."""
    fake_path = "missing_columns.xlsx"
    # DataFrame в котором вообще нет колонки 'id' и 'amount'
    wrong_mock_data = {
        "state": ["EXECUTED"],
        "date": ["2026-10-27"],
        # колонка 'id' отсутствует
    }
    wrong_df = pd.DataFrame(wrong_mock_data)
    with patch.object(Path, "is_file", return_value=True), patch("pandas.read_excel", return_value=wrong_df):
        result = parse_xlsx_with_pandas(fake_path)
    assert result == "error excel data format"
