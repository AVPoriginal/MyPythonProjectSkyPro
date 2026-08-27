import pytest

from src.processing import filter_by_state, sort_by_date

# Перенес в conftest.py

test_data_list = [
    {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},  # нет ключа state
    {"id": 939719570, "state": "EXECUTED"},  # нет ключа date
    {"id": 594226727, "state": "CANCELED", "date": 241689},  # дата не строка
    {"id": 615064591, "state": "CANCELED", "date": "абракодабра"},  # дата не ISO
    {"id": 414288292, "state": "EXECUTED", "date": ""},  # дата пустая
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 9397195702, "state": "EXECUTED", "date": "2027-06-30T02:08:58.425572"},
    {"id": 5942267272, "state": "CANCELED", "date": "2020-09-12T21:27:25.241689"},
    {"id": 6150645912, "state": "CANCELED", "date": "2021-10-14T08:21:33.419441"},
]

test_data_list_canceled = [
    {"id": 594226727, "state": "CANCELED", "date": 241689},  # дата не строка
    {"id": 615064591, "state": "CANCELED", "date": "абракодабра"},  # дата не ISO
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 5942267272, "state": "CANCELED", "date": "2020-09-12T21:27:25.241689"},
    {"id": 6150645912, "state": "CANCELED", "date": "2021-10-14T08:21:33.419441"},
]

test_data_list_executed = [
    {"id": 939719570, "state": "EXECUTED"},
    {"id": 414288292, "state": "EXECUTED", "date": ""},  # дата пустая
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 9397195702, "state": "EXECUTED", "date": "2027-06-30T02:08:58.425572"},
]

test_data_list_up = [
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 5942267272, "state": "CANCELED", "date": "2020-09-12T21:27:25.241689"},
    {"id": 6150645912, "state": "CANCELED", "date": "2021-10-14T08:21:33.419441"},
    {"id": 9397195702, "state": "EXECUTED", "date": "2027-06-30T02:08:58.425572"},
]


test_data_list_down = [
    {"id": 9397195702, "state": "EXECUTED", "date": "2027-06-30T02:08:58.425572"},
    {"id": 6150645912, "state": "CANCELED", "date": "2021-10-14T08:21:33.419441"},
    {"id": 5942267272, "state": "CANCELED", "date": "2020-09-12T21:27:25.241689"},
    {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
]
# print(sort_by_date(in_listtest, False))

# пока не понял как красиво параметризовать когда не передает параметра по умолчанию
# @pytest.mark.parametrize("data_list, expected_result, sorting", [
#     (test_data_list, test_data_list_executed, 'EXECUTED'),
#     (test_data_list, test_data_list_executed, 'EXECUTED'),
#     (test_data_list, test_data_list_canceled, 'CANCELED'),
#     ])
# def test_filter_by_state(data_list, sorting, expected_result):
#     assert filter_by_state(data_list, sorting) == expected_result


# проверка сортировки по статусу по умолчанию
def test_filter_by_default():
    assert filter_by_state(test_data_list) == test_data_list_executed


# проверка сортировки по статусу executed
def test_filter_by_executed():
    assert filter_by_state(test_data_list, "EXECUTED") == test_data_list_executed


# проверка сортировки по статусу canceled
def test_filter_by_canceled():
    assert filter_by_state(test_data_list, "CANCELED") == test_data_list_canceled


# проверка сортировки по дате по умолчанию - сначала новые
def test_sort_by_date_default():  #
    assert sort_by_date(test_data_list) == test_data_list_down


# проверка сортировки по дате - сначала новые
def test_sort_by_date_down():
    assert sort_by_date(test_data_list, True) == test_data_list_down


# проверка сортировки по дате  - сначала старые
def test_sort_by_date_up():
    assert sort_by_date(test_data_list, False) == test_data_list_up