
############################
# module for homework 11.1 #
############################

from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    принимает список словарей с транзакциями и код заданной валюты,
    возвращает транзакции с заданным кодом валюты.
    если требуемое значение ключа в словаре отсутствует, игнорирует транзакцию
    """

    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
                yield transaction
        except KeyError, TypeError, AttributeError:
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    принимает список словарей с транзакциями,
    возвращает строку описания транзакции из словаря
    если поле описания в словаре отсутствует, возвращает пустую
    """
    if not transactions:
        yield ""
        return
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            yield description
        except KeyError, TypeError:
            yield ""


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    принимает десятичные целые начальное и конечное значение диапазона
    генерирует 16 значный номер карты, возвращает строку в формате
    представления номера карты - четыре октета через пробел
    при некорректном задании диапазона возвращает ошибку
    "Некорректное задание диапазона номеров"
    """

    if (
        not isinstance(start, int)
        or isinstance(start, bool)
        or not isinstance(end, int)
        or isinstance(end, bool)
        or start < 1
        or end > 9999999999999999
        or start > end
    ):
        yield "Некорректное задание диапазона номеров"
        return
    for number in range(start, end + 1):
        string_number_card = " ".join(f"{number:016d}"[i : i + 4] for i in range(0, 16, 4))
        yield string_number_card
