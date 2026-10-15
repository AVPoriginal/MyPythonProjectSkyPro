##################################
# module utils for homework 12.1 #
##################################

import json
from pathlib import Path
from typing import Any


def get_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """
    принимает файл json с финансовыми транзакциями и возвращает список словарей
    если файл пустой содержит не список или не найден возвращает пустой список
    """

    path = Path(file_path)

    # проверка существует ли файл
    if not path.is_file():
        return []
    try:
        # открываем файл и пытаемся десериализовать json
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # проверка структуры - данные должны быть спиcском а элементы словарями
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return data
        return []

    except (json.JSONDecodeError, PermissionError):
        # в случае ошибки json или отсутствия прав доступа
        return []


# выполнится только при прямом запуске файла
if __name__ == '__main__':
    print("Проверка функции: if __name__ == '__main__':")
    # формируется путь к файлу
    BASE_DIR = Path(__file__).resolve().parent.parent
    path_to_json = BASE_DIR / "data" / "operations.json"
    print(get_transactions(path_to_json))


#     # еще вариант проверки сравнить скорость
#     if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
#         return []
