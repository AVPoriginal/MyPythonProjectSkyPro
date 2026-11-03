import pytest

from src.masks import get_mask_account, get_mask_card_number

# Перенес в conftest.py
# test_data_card_number = [
#             ("1234567890123456", "1234 56** **** 3456"),
#             ("12345678901234566", "данные не верны!"),
#             ("1234567", "данные не верны!"),
#             ("123456789012345A", "данные не верны!"),
#            ]
#
# @pytest.fixture(params=test_data_card_number)
# def case_data_card_number(request):
#   # request.param поочередно принимает каждый кортеж из test_data_card_number
#   return request.param
#
# test_data_account = [("1234567890123456", "**3456"),
#              ("A345678901234566", "данные не верны!"),
#              ("123", "данные не верны!")
#             ]
#
# @pytest.fixture(params=test_data_account)
# def case_data_account(request):
# # request.param поочередно принимает каждый кортеж из test_data_account
#    return request.param


# Тест автоматически запустится по разу для каждого кортежа из test_data...


def test_get_mask_card_number(case_data_card_number):
    in_card, expected = case_data_card_number
    assert get_mask_card_number(in_card) == expected


def test_get_mask_account(case_data_account):
    in_account, expected = case_data_account
    assert get_mask_account(in_account) == expected
