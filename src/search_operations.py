############################
# module for homework 13.2 #
############################

import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    возвращает список транзакций в описании которых найдена указанная подстрока.
    поиск выполняется регистронезависимо
    """
    # re.escape экранирует спецсимволы
    # re.IGNORECASE делает поиск нечувствительным к регистру
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [item for item in data if pattern.search(str(item.get("description") or ""))]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    принимает список словарей с банковскими операциями, список категорий для подсчета
    подсчитывает количество операций для каждой категории с использованием collections.Counter
    возвращает словарь {категория: количество}
    """
    # Counter автоматически игнорирует отсутствующие ключи возвращая 0
    counts = Counter(tr.get("description") for tr in data)
    # итоговый словарь в порядке переданных категорий
    return {cat: counts[cat] for cat in categories}

