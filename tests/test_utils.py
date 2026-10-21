
import json
from pathlib import Path

from src.utils import get_transactions

#####
# 1


def test_get_transactions_success(tmp_path):
    """ тест чтения корректного json файла """
    # временный файл
    file_path = tmp_path / "valid.json"
    # запись корректных данных
    mock_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    file_path.write_text(json.dumps(mock_data), encoding="utf-8")

    result = get_transactions(file_path)
    assert result == mock_data
    assert len(result) == 2


#####
# 2

def test_get_transactions_file_not_found():
    """ тест когда файл не существует """
    # несуществующий файл
    non_existent_path = Path("data/file_not_found.json")

    result = get_transactions(non_existent_path)
    assert result == []


#####
# 3

def test_get_transactions_empty_file(tmp_path):
    """ тест с пустым файлом """
    file_path = tmp_path / "empty.json"
    # делаем пустой файл
    file_path.write_text("", encoding="utf-8")

    result = get_transactions(file_path)
    assert result == []


#####
# 4

def test_get_transactions_not_a_list(tmp_path):
    """ тест когда в .json не список """
    file_path = tmp_path / "dict.json"
    # словарь вместо списка
    mock_data = {"status": "success", "data": []}
    file_path.write_text(json.dumps(mock_data), encoding="utf-8")

    result = get_transactions(file_path)
    assert result == []


#####
# 5

def test_get_transactions_list_with_invalid_items(tmp_path):
    """ тест когда в json список но элементы не словари """
    file_path = tmp_path / "invalid_items.json"
    # строки и числа вместо словарей
    mock_data = [100500, "string_item", {"valid_dict": True}]
    file_path.write_text(json.dumps(mock_data), encoding="utf-8")

    result = get_transactions(file_path)
    assert result == []


#####
# 7

def test_get_transactions_corrupted_json(tmp_path):
    """ тест битого json """
    file_path = tmp_path / "corrupted.json"
    # сломанный json без закрывающей скобки
    file_path.write_text('[{"id": 1}', encoding="utf-8")

    result = get_transactions(file_path)
    assert result == []
