
import sys
import logging # было использовано в задании 12.2
import os # было использовано в задании 12.2
# import pytest # было использовано в задании 12.2
from pathlib import Path
from src.parse_transactions import parse_csv_with_pandas, parse_xlsx_with_pandas
from src.utils import get_transactions
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency
from src.widget import mask_account_card, get_date
from src.search_operations import process_bank_search


def setup_logging():
    """
    настройка логеров для модулей masks и utils
    запись логов ведется в файл по пути logs/log_app.log
    если путь не существует, то будет создан
    файл лога обновляется при каждом запуске
    """
    log_dir = "logs"
    log_file = os.path.join(log_dir, "log_app.log")
    os.makedirs(log_dir, exist_ok=True)

    # очистка файла перед стартом приложения
    with open(log_file, "w", encoding="utf-8") as f:
        f.truncate(0)

    # настройки логирования для модуля masks
    logger_masks = logging.getLogger("applog.masks")
    logger_masks.setLevel(logging.DEBUG)
    logger_masks.propagate = False

    handler_masks = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    handler_masks.setFormatter(
        logging.Formatter("[модуль masks] %(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
    )
    logger_masks.addHandler(handler_masks)

    # настройки логирования для модуля utils
    logger_utils = logging.getLogger("applog.utils")
    logger_utils.setLevel(logging.DEBUG)
    logger_utils.propagate = False

    handler_utils = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    handler_utils.setFormatter(
        logging.Formatter(
            "[модуль utils] [функция: %(funcName)s] %(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S"
        )
    )
    logger_utils.addHandler(handler_utils)

# настройка логирования
setup_logging()

# настройка путей к файлам данных
BASE_DIR = Path(__file__).resolve().parent
path_to_csv = BASE_DIR / "data" / "transactions.csv"
path_to_xlsx = BASE_DIR / "data" / "transactions_excel.xlsx"
path_to_json = BASE_DIR / "data" / "operations.json"


def format_transactions(transactions: list[dict]):
    """ форматирует и выводит список словарей в формате задания 13.2 """
    for tr in transactions:
        date_str = get_date(tr.get("date")) #привод даты к формату вывода
        description = tr.get("description", "")
        # маскировка вывода счетов и карт
        # проверка если в поле данных попадается None или NaN
        source = tr.get("from", "")
        destination = tr.get("to", "")
        if source is None or source != source :
            source = ""
        if destination is None or destination != destination :
            destination = ""
        else:
            destination = mask_account_card(destination)
        tr_amount = tr.get("operationAmount", {})
        amount = tr_amount.get("amount", 0.0)
        currency_code = tr_amount.get("currency", {}).get("code", "")
        # вывод в консоль
        print(f"{date_str} {description}")
        if source == "" :
            print(f"{destination}")
        else :
            print(f"{mask_account_card(source)} -> {destination}")
        print(f"Сумма: {amount} {currency_code}")
        print()  # строка для разделения транзакций


print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
while True:
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    print("4. Выйти из программы")
    user_input = input("\nВаш выбор: ")
    if user_input == "1":
        print("\nДля обработки выбран JSON-файл.")
        load_transactions = get_transactions(path_to_json)
        break  # выход из цикла
    elif user_input == "2":
        print("\nДля обработки выбран CSV-файл.")
        load_transactions = parse_csv_with_pandas(path_to_csv)
        break  # выход из цикла
    elif user_input == "3":
        print("\nДля обработки выбран XLSX-файла.")
        load_transactions = parse_xlsx_with_pandas(path_to_xlsx)
        break  # выход из цикла
    elif user_input == "4":
        print("\nвыход из программы")
        sys.exit()  # прерывает выполнение программы
    else:
        print("\n Некорректный выбор. Пожалуйста, попробуйте еще раз.")


while True:
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
          "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
    print("Чтобы выйти из программы введите exit")
    user_input = input("\nВведите: ")
    if user_input.upper() == "EXECUTED":
        print("\n Операции отфильтрованы по статусу EXECUTED ")
        output_transactions = filter_by_state(load_transactions)
        break  # выход из цикла
    elif user_input.upper() == "CANCELED":
        print("\n Операции отфильтрованы по статусу CANCELED ")
        output_transactions = filter_by_state(load_transactions, user_input.upper())
        break  # выход из цикла
    elif user_input.upper() == "PENDING":
        print("\n Операции отфильтрованы по статусу PENDING ")
        output_transactions = filter_by_state(load_transactions, user_input.upper())
        break  # выход из цикла
    elif user_input.lower().strip() == "exit":
        print("\nвыход из программы")
        sys.exit()  # прерывает выполнение программы
    else:
        print(f"\n: Некорректный выбор. Статус операции {user_input} недоступен. \n "
                                                             "Пожалуйста, попробуйте еще раз.")


while True:
    print("\nОтсортировать операции по дате? Да(Yes)/Нет(No)")
    print("Чтобы выйти из программы введите exit или выход")
    user_input = input("\nВведите: ")
    if user_input.upper().strip() in ["ДА", "YES"]:
        while True:
            print("\nОтсортировать по возрастанию или по убыванию?")
            print("Чтобы выйти из программы введите exit или выход")
            user_input2 = input("\nВведите возрастанию/убыванию: ")
            if user_input2.lower().strip() == "возрастанию":
                print("\n Операции отфильтрованы по возрастанию даты ")
                output_transactions = sort_by_date(output_transactions, False)
                break  # выход из цикла
            if user_input2.lower().strip() == "убыванию":
                print("\n Операции отфильтрованы по убыванию даты ")
                output_transactions = sort_by_date(output_transactions)
                break  # выход из цикла
            elif user_input2.lower().strip() in ["exit", "выход"]:
                print("\n выход из программы")
                sys.exit()  # прерывает выполнение программы
            else:
                print("\n: Некорректный выбор. "
                      "Выберите сортировку даты или выход из программы \n "
                      "Пожалуйста, попробуйте еще раз.")
        break  # выход из цикла
    elif user_input.upper().strip() in ["НЕТ", "NO"]:
        print("\n Операции не соритрованы по дате ")
        break  # выход из цикла
    elif user_input.lower().strip() in ["exit", "выход"]:
        print("\n выход из программы")
        sys.exit()  # прерывает выполнение программы
    else:
        print("\n: Некорректный выбор. Выберите сортировку даты или выход из программы \n "
                      "Пожалуйста, попробуйте еще раз.")


while True:
    print("\nВыводить только рублевые транзакции? Да(Yes)/Нет(No)")
    print("Чтобы выйти из программы введите exit или выход")
    user_input = input("\n Введите : ")
    if user_input.upper().strip() in ["ДА", "YES"]:
        print("\n Операции только в рублях ")
        output_transactions = list(filter_by_currency(output_transactions,"RUB"))
        break  # выход из цикла
    elif user_input.upper().strip() in ["НЕТ", "NO"]:
        print("\n Выводятся операции с любой валютой")
        break  # выход из цикла
    elif user_input.lower().strip() in ["exit", "выход"]:
        print("\nвыход из программы")
        sys.exit()  # прерывает выполнение программы
    else:
        print("\n: Некорректный выбор. Выберите все или только в рублях или выход из программы \n "
                      "Пожалуйста, попробуйте еще раз.")


while True:
    print("\nОтфильтровать список транзакций по определенному слову/строке"
          " в описании? Да(Yes)/Нет(No)")
    print("Чтобы выйти из программы введите exit или выход")
    user_input = input("\nПользователь: ")
    if user_input.upper().strip() in ["ДА", "YES"]:
        print("Введите строку для поиска в описании транзакции:")
        user_input = input("\nВведите: ")
        print(f"\n Операции отфильтрованы по слову/строке: {user_input}")
        output_transactions = process_bank_search(output_transactions, user_input)
        break  # выход из цикла
    elif user_input.upper().strip() in ["НЕТ", "NO"]:
        print("\n Выводятся операции с любой валютой")
        break  # выход из цикла
    elif user_input.lower().strip() in ["exit", "выход"]:
        print("\nвыход из программы")
        sys.exit()  # прерывает выполнение программы
    else:
        print("\n: Некорректный выбор. Выберите все или только в рублях или выход из программы \n "
                      "Пожалуйста, попробуйте еще раз.")

if len(output_transactions) == 0:
    print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
else:
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(output_transactions)}")
    format_transactions(output_transactions)


# ниже было использовано для задания 12.2 на данный момент не требуется
#
# if __name__ == "__main__":
#     # настройка логирования
#     setup_logging()
#     print("Логирование сконфигурировано. Запуск pytest...")
#
#     # запуск тестов
#     pytest.main(["-s", "-v"])
