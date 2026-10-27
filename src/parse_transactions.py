###############################################
# module parse_transactions for homework 13.1 #
###############################################

from pathlib import Path
from typing import Any

import pandas as pd


def parse_csv_with_pandas(file_path: str | Path) -> list[dict[str, Any]] | str:
    """
    Принимает файл csv с финансовыми транзакциями и возвращает список словарей транзакций
    если файл не найден -  возвращает строку 'file not found'
    пустой - 'file is empty'
    содержит только заголовки — 'no data in file'
    обязательные поля данных транзакций 'id', 'state', 'date', 'amount', 'currency_name', 'currency_code'
    если их нет возвращает - "error csv data format"
    если файл поврежден или имеет неверный формат — возвращает строку "error csv format".
    """
    path = Path(file_path)
    # проверка существует ли файл
    if not path.is_file():
        return "file not found"
    try:
        # читаем файл
        df = pd.read_csv(path, sep=";")
        # если в файле только заголовки DataFrame будет пустым 0 строк
        if df.empty:
            return "no data in file"
        # список обязательных колонок без которых структура транзакции сломается
        required_columns = {"id", "state", "date", "amount", "currency_name", "currency_code"}
        # проверка что все нужные колонки присутствуют в CSV
        if not required_columns.issubset(df.columns):
            return "error csv data format"
    except pd.errors.EmptyDataError:
        # если файл абсолютно пустой - 0 байт
        return "file is empty"
    except pd.errors.ParserError, Exception:
        # pd.errors.ParserError ловит ошибки структуры например разное количество полей в строках
        # Exception подстраховывает от других непредвиденных ошибок чтения
        return "error csv format"
    # заменяем все NaN/NaT на None для корректной выгрузки в словари
    df = df.where(pd.notnull(df), None)

    result = []
    for _, row in df.iterrows():
        item = {
            "id": row.get("id"),
            "state": row.get("state"),
            "date": row.get("date"),
            "operationAmount": {
                "amount": row["amount"],
                "currency": {
                    "name": row.get("currency_name"),
                    "code": row.get("currency_code"),
                },
            },
            "description": row.get("description"),
            "from": row.get("from") if row.get("from") else None,
            "to": row.get("to") if row.get("to") else None,
        }
        result.append(item)
    return result


def parse_xlsx_with_pandas(file_path: str | Path) -> list[dict[str, Any]] | str:
    """
    Принимает файл excel с финансовыми транзакциями и возвращает список словарей транзакций
    если файл не найден -  возвращает строку 'file not found'
    пустой - 'file is empty'
    содержит только заголовки или лист полностью пуст— 'no data in file'
    обязательные поля данных транзакций 'id', 'state', 'date', 'amount', 'currency_name', 'currency_code'
    если их нет возвращает - "error excel data format"
    если файл поврежден или имеет неверный формат — возвращает строку "error excel format".
    """
    path = Path(file_path)
    if not path.is_file():
        return "file not found"
    try:
        # читаем файл excel (по умолчанию используется движок openpyxl)
        df = pd.read_excel(path)
        # если в файле были только заголовки или лист полностью пуст
        if df.empty:
            return "no data in file"
        # список обязательных колонок без которых структура транзакции сломается
        required_columns = {"id", "state", "date", "amount", "currency_name", "currency_code"}
        # проверяем что все нужные колонки присутствуют на листе Excel
        if not required_columns.issubset(df.columns):
            return "error excel data format"
    except ValueError:
        # Pandas выбрасывает ValueError если файл Excel абсолютно пустой (0 байт)
        # или в нем нет ни одного читаемого листа/заголовка
        return "file is empty"
    except Exception:
        # любые другие ошибки (битый zip-архив xlsx, отсутствие openpyxl, неверный формат)
        return "error excel format"
    # заменяем все NaN/NaT на None для корректной выгрузки в словари
    df = df.where(pd.notnull(df), None)

    result = []
    for _, row in df.iterrows():
        item = {
            "id": row.get("id"),
            "state": row.get("state"),
            "date": row.get("date"),
            "operationAmount": {
                "amount": row.get("amount"),
                "currency": {
                    "name": row.get("currency_name"),
                    "code": row.get("currency_code"),
                },
            },
            "description": row.get("description"),
            "from": row.get("from") if row.get("from") else None,
            "to": row.get("to") if row.get("to") else None,
        }
        result.append(item)
    return result


# выполнится только при прямом запуске файла
if __name__ == "__main__":
    print("Проверка функций модуля: if __name__ == '__main__':")

    # формируется путь к файлу
    BASE_DIR = Path(__file__).resolve().parent.parent

    path_to_csv = BASE_DIR / "data" / "transactions.csv"
    print(parse_csv_with_pandas(path_to_csv))

    path_to_xlsx = BASE_DIR / "data" / "transactions_excel.xlsx"
    print(parse_xlsx_with_pandas(path_to_xlsx))
