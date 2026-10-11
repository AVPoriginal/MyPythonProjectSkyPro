from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

#
# Фикстуры для тестирования функций filter_by_currency, transaction_descriptions модуля generators
#


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def invalid_transactions() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями, имеющими некорректную структуру."""
    return [
        {"id": 1, "wrong_key": "test"},  # Нет operationAmount
        {"id": 2, "operationAmount": {"amount": "100"}},  # Нет currency
        {"id": 3, "operationAmount": {"currency": {"code": 123}}},  # code не строка
        {"id": 4, "operationAmount": "not a dict"},  # operationAmount не словарь
        {"id": 5},  # Пустой словарь
    ]


@pytest.fixture
def mixed_transactions() -> List[Dict[str, Any]]:
    """Фикстура со смешанными корректными и некорректными транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {"wrong_field": "Некорректная"},
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {},
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


@pytest.fixture
def test_list_transactions() -> List[Dict[str, Any]]:
    """
    Фикстура данных транзакций из примера задания
    """
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


###############################################################################
# тесты filter_by_currency


def test_filter_by_currency(test_list_transactions):
    """
    тест filter_by_currency с валидными данными списка транзакций из примера задания
    """
    generator1 = filter_by_currency(test_list_transactions, "USD")
    assert next(generator1) == {
        "date": "2018-06-30T02:08:58.425572",
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "id": 939719570,
        "operationAmount": {"amount": "9824.07", "currency": {"code": "USD", "name": "USD"}},
        "state": "EXECUTED",
        "to": "Счет 11776614605963066702",
    }
    assert next(generator1) == {
        "date": "2019-04-04T23:20:05.206878",
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "id": 142264268,
        "operationAmount": {"amount": "79114.93", "currency": {"code": "USD", "name": "USD"}},
        "state": "EXECUTED",
        "to": "Счет 75651667383060284188",
    }
    assert next(generator1) == {
        "date": "2018-08-19T04:27:37.904916",
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "id": 895315941,
        "operationAmount": {"amount": "56883.54", "currency": {"code": "USD", "name": "USD"}},
        "state": "EXECUTED",
        "to": "Visa Platinum 8990922113665229",
    }
    try:
        next(generator1)
        assert False, "Expected StopIteration"
    except StopIteration:
        pass


def test_filter_by_currency_empty(empty_transactions):
    """
    тест filter_by_currency с пустым списком транзакций
    """
    assert len(list(filter_by_currency(empty_transactions, "USD"))) == 0


def test_filter_by_currency_invalid(invalid_transactions):
    """
    тест filter_by_currency с невалидными данными в словарях списка транзакций
    """
    assert len(list(filter_by_currency(invalid_transactions, "USD"))) == 0


def test_filter_by_currency_mixed(mixed_transactions):
    """
    тест filter_by_currency с валидными и невалидными данными в словарях транзакций списка
    """
    generator = filter_by_currency(mixed_transactions, "USD")
    assert next(generator) == {
        "date": "2018-06-30T02:08:58.425572",
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "id": 939719570,
        "operationAmount": {"amount": "9824.07", "currency": {"code": "USD", "name": "USD"}},
        "state": "EXECUTED",
        "to": "Счет 11776614605963066702",
    }
    assert next(generator) == {
        "date": "2019-04-04T23:20:05.206878",
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "id": 142264268,
        "operationAmount": {"amount": "79114.93", "currency": {"code": "USD", "name": "USD"}},
        "state": "EXECUTED",
        "to": "Счет 75651667383060284188",
    }
    try:
        next(generator)
        assert False, "Expected StopIteration"
    except StopIteration:
        pass


###############################################################################
# тесты transaction_descriptions


def test_transaction_descriptions(test_list_transactions):
    """
    тест transaction_descriptions с валидными данными списка транзакций из примера задания
    """
    generator = transaction_descriptions(test_list_transactions)
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод с карты на карту"
    assert next(generator) == "Перевод организации"
    try:
        next(generator)
        assert False, "Expected StopIteration"
    except StopIteration:
        pass


def test_transaction_descriptions_empty(empty_transactions):
    """
    тест transaction_descriptions с пустым списком транзакций
    """
    assert next(transaction_descriptions(empty_transactions)) == ""


def test_transaction_descriptions_invalid(invalid_transactions):
    """
    тест transaction_descriptions с невалидными данными списка транзакций
    """
    assert next(transaction_descriptions(invalid_transactions)) == ""


def test_transaction_descriptions_mixed(mixed_transactions):
    """
    тест transaction_descriptions с валидными и невалидными данными списка транзакций
    """
    generator = transaction_descriptions(mixed_transactions)
    assert next(generator) == "Перевод организации"
    assert next(generator) == ""
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == ""
    assert next(generator) == "Перевод со счета на счет"
    try:
        next(generator)
        assert False, "Expected StopIteration"
    except StopIteration:
        pass


###############################################################################
# тесты card_number_generator
#


# # декоратор параметризации для теста функции card_number_generator
@pytest.mark.parametrize(
    "startnumber, endnumber, expected",
    [
        (1, 1, "0000 0000 0000 0001"),
        (100, 100, "0000 0000 0000 0100"),
        (True, 1, "Некорректное задание диапазона номеров"),
        (1, False, "Некорректное задание диапазона номеров"),
        ("1", True, "Некорректное задание диапазона номеров"),
        ("1", "1", "Некорректное задание диапазона номеров"),
        (True, True, "Некорректное задание диапазона номеров"),
    ],
)
def test_card_number_generator_valueerror(startnumber, endnumber, expected):
    """
    тест итератора card_number_generator при валидных входных данных
    """
    generator = card_number_generator(startnumber, endnumber)
    assert next(generator) == expected


def test_card_number_generator():
    """
    тест итератора card_number_generator при валидных входных данных
    """
    generator = card_number_generator(1, 5)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"
    assert next(generator) == "0000 0000 0000 0004"
    assert next(generator) == "0000 0000 0000 0005"
    try:
        next(generator)
        assert False, "Expected StopIteration"
    except StopIteration:
        pass
