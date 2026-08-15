# module for homework 10.1

from typing import Any
from datetime import datetime

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




def sort_by_date(list_for_sorting: list[dict[str, Any]], sorting_order: bool = True) -> list[dict[str, Any]] :

    """
    принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """

    sorted_list = sorted(list_for_sorting, key=lambda x: datetime.fromisoformat(x["date"].replace('Z', '+00:00')), reverse = sorting_order)
    return sorted_list

in_listtest=[
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    , {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    , {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
    , {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

print(filter_by_state(in_listtest))
print(sort_by_date(in_listtest))

