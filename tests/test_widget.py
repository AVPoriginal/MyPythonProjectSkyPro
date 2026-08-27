from datetime import datetime

import pytest

from src.widget import get_date, mask_account_card

# print(get_date("2024-03-11T02:26:18.671407"))
# print(mask_account_card("Visa Platinum Счет 1234567890123456"))

# Перенес в conftest.py
# test_data_mask_account = [
#             ("Visa Platinum Счет 1234567890123456", "данные не верны"), # не правильная подпись к номеру
#             ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),   # правильные данные карты
#             ("Счет 1234567890123456", "Счет **3456"),                  # правильные данные счета
#             ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),     # правильные данные карты
#             ("Visa Platinum 12345678901234567", "данные не верны"),    # больше цифр в номере карты
#             ("", "данные не верны"),                    # пустая строка
#             ("                ", "данные не верны"),    # одни пропуски
#             ("Visa Platinum", "данные не верны"),    # отсутствует номер карты
#             ("Счет", "данные не верны"),             # отсутствует номер счета
#             ("Счет 123", "данные не верны"), # номер счета меньше 4
#             ("Visa Platinum 1234567890123", "данные не верны"), # номер карты меньше 16
#             ("Visa Platinum @234567890123456", "данные не верны"), # спецсимволы в номере карты
#             ("Счет @234567890123456", "данные не верны"), # спецсимволы в номере счета
#             ("      1234567890123456", "данные не верны"), # отсутствует подпись к номеру
#            ]
#
# test_data_date = [("2024-03-11T02:26:18.671407", "11.03.2024"),    # правильные данные
#              ("2024-03-11", "11.03.2024"),          # правильные данные
#              ("2024-03-11T02:26", "11.03.2024"),    # правильные данные
#              ("-2024-03-11T02:26:18.671407", None), # не корректная запись
#              ("2024-13-11T02:26:18.671407", None),  # не корректная запись
#              ("2024-03-35T02:26:18.671407", None),  # не корректная запись
#              ("2024-03-11T25:26:18.671407", None),  # не корректная запись
#              ("", None),                            # пустая строка
#              ("                ", None),            # пробелы
#              ("tupe T02:26:18.671407", None),       # не корректная запись
#             ]
#
#
# @pytest.fixture(params=test_data_mask_account)
# def case_data_mask_account(request):
#   # request.param поочередно принимает каждый кортеж из test_data_mask_account
#   return request.param
#
#
# @pytest.fixture(params=test_data_date)
# def case_data_date(request):
# # request.param поочередно принимает каждый кортеж из test_data_date
#    return request.param


# Тест автоматически запустится по разу для каждого кортежа из test_data...


def test_get_mask_account_card(case_data_mask_account):
    in_account, expected = case_data_mask_account
    assert mask_account_card(in_account) == expected


def test_get_date(case_data_date):
    in_data, expected = case_data_date
    assert get_date(in_data) == expected
