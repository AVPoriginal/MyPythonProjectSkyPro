# module for homework 10.1

from datetime import datetime
from typing import Any


def filter_by_state(in_list_operations: list[dict[str, Any]], concept_state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
     принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED').
     возвращает новый список словарей содержащий только те словари
     у которых ключ state соответствует указанному значению.
    """

    # стоит проверить варианты написания функции ниже на использование ресурсов
    # и выбрать на будущее более подходящий

    # filtered_list = list(filter(lambda x: x.get("state") == concept_state, in_list_operations))
    filtered_list = [item for item in in_list_operations if item.get("state") == concept_state]
    return filtered_list


def sort_by_date(list_for_sorting: list[dict[str, Any]], sorting_order: bool = True) -> list[dict[str, Any]]:
    """
    принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    функция возвращает новый список, отсортированный по дате (date)
    если поле даты некорректно, словарь исключается из обработки и выдачи
    использует вспомогательную функцию is_valid_iso_date (в этом же модуле)
    """

    clean_bad_data = list(filter(is_valid_iso_date, list_for_sorting))
    sorted_list = sorted(
        clean_bad_data, key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "+00:00")), reverse=sorting_order
    )
    return sorted_list


# Вспомогательная функция определения некорректной даты
def is_valid_iso_date(item: dict[str, Any]) -> bool:
    """
    Принимает словарь,
    Возвращает True, если дата существует и корректна, иначе False.
    """
    date_str = item.get("date")
    if not date_str or not isinstance(date_str, str):
        return False
    try:
        datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

    # Ниже шаблоны для быстрого теста

# in_listtest=[
#     {'id': 41428829, 'date': '2019-07-03T18:35:29.512364'} # нет ключа state
#     , {'id': 939719570, 'state': 'EXECUTED'}  # нет ключа date
#     , {'id': 594226727, 'state': 'CANCELED', 'date': 241689} # дата не строка
#     , {'id': 615064591, 'state': 'CANCELED', 'date': 'абракодабра'} # дата не ISO
#     , {'id': 414288292, 'state': 'EXECUTED', 'date': ''} # дата пустая
#     , {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
#     , {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
#     , {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
#     , {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
#     , {'id': 9397195702, 'state': 'EXECUTED', 'date': '2027-06-30T02:08:58.425572'}
#     , {'id': 5942267272, 'state': 'CANCELED', 'date': '2020-09-12T21:27:25.241689'}
#     , {'id': 6150645912, 'state': 'CANCELED', 'date': '2021-10-14T08:21:33.419441'}
# ]
#
# print(filter_by_state(in_listtest))
# print(filter_by_state(in_listtest, 'CANCELED'))
# print(sort_by_date(in_listtest))
# print(sort_by_date(in_listtest, False))
