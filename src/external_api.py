#########################################
# module external_api for homework 12.1 #
#########################################

import os
import requests
from typing import Any
from dotenv import load_dotenv

# загрузка переменных из .env файла
load_dotenv()

EXCHANGERATES_API_KEY = os.getenv('EXCHANGERATES_API_KEY')


def get_amount_in_rub(transaction: dict[str, Any]) -> float:
    """
    принимает словарь транзакции, возвращает сумму amount в рублях в формате float
    если валюта отличная от RUB конвертирует её через Exchange Rates Data API.
    """
    # извлекаем сумму и валюту из словаря транзакции
    operation_amount_data = transaction.get("operationAmount", {})
    amount_str = operation_amount_data.get("amount", "0")
    amount = float(amount_str)
    currency_data = operation_amount_data.get("currency", {})
    currency_code = currency_data.get("code", "RUB").upper()

    # 2. Если валюта уже рубли, возвращаем float сумму без запросов к API
    if currency_code == "RUB":
        return amount

    # 3. Если валюта USD, EUR или любая другая, делаем запрос к API
    url = "https://api.apilayer.com/exchangerates_data/convert"

    headers = {
        "apikey": EXCHANGERATES_API_KEY
    }
    params = {
        "from": currency_code,
        "to": "RUB",
        "amount": amount
    }

    try:
        # Делаем запрос к эндпоинту конвертации
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Вызовет ошибку, если HTTP-статус не 200

        data = response.json()

        if data.get("success"):
            # API возвращает готовый результат в поле 'result'
            return float(data["result"])
        else:
            raise RuntimeError(f"Ошибка API при конвертации: {data}")

    except requests.exceptions.RequestException as e:
        # Обработка сетевых ошибок (тайм-ауты, проблемы с соединением)
        raise RuntimeError(f"Не удалось подключиться к API конвертации валют: {e}")

# выполнится только при прямом запуске файла
if __name__ == '__main__':
    print("Проверка функции: if __name__ == '__main__':")
    tx_rub = {'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041', 'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}}, 'description': 'Перевод организации', 'from': 'Maestro 1596837868705199', 'to': 'Счет 64686473678894779589'}
    print(f"Сумма указана в рублях: {get_amount_in_rub(tx_rub)}")

    tx_usd = {'id': 142264268, 'state': 'EXECUTED', 'date': '2019-04-04T23:20:05.206878', 'operationAmount': {'amount': '79114.93', 'currency': {'name': 'USD', 'code': 'USD'}}, 'description': 'Перевод со счета на счет', 'from': 'Счет 19708645243227258542', 'to': 'Счет 75651667383060284188'}
    try:
        amount_in_rub = get_amount_in_rub(tx_usd)
        print(f"Сумма в рублях: {amount_in_rub} ")
    except RuntimeError as err:
        print(f"Произошла ошибка: {err}")




