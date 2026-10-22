import logging

#  for homework 12.2 add logger
#  логгер модуля (настройка в main.py)
logger = logging.getLogger("applog.masks")


def get_mask_card_number(in_card_number: str) -> str:
    """принимает на вход номер карты и возвращает ее маску
    Номер карты замаскирован и отображается в формате
    XXXX XX** **** XXXX , где X — это цифра номера.
    То есть видны первые 6 цифр и последние 4 цифры,
    остальные символы отображаются звездочками,
    номер разбит по блокам по 4 цифры, разделенным пробелами.
    Пример работы функции:
    7000792289606361     # входной аргумент
    7000 79** **** 6361  # выход функции
    """

    logger.info("обращение к функции")
    logger.debug("В функцию передан номер: %s", in_card_number)
    out_card_number_mask = ""
    if in_card_number.isdigit() and (len(in_card_number) == 16):
        out_card_number_mask = in_card_number[0:4] + " " + in_card_number[4:6] + "** **** " + in_card_number[12:16]
        logger.debug("Результат вычислен. Функция возвратила: %s", out_card_number_mask)
    else:
        out_card_number_mask = "данные не верны!"
        logger.error("Входные данные не число 16 цифр. Функция возвратила: %s", out_card_number_mask)
    return out_card_number_mask


def get_mask_account(in_account: str) -> str:
    """
    принимает на вход номер счета и возвращает его маску.
    Номер счета замаскирован и отображается в формате
    **XXXX , где X — это цифра номера.
    То есть видны только последние 4 цифры номера, а перед ними — две звездочки.
    Пример работы функции:
    73654108430135874305  # входной аргумент
    **4305  # выход функции
    """

    logger.info("обращение к функции")
    logger.debug("В функцию передан номер: %s", in_account)
    out_account_mask = ""
    if in_account.isdigit() and (len(in_account) >= 4):
        out_account_mask = "**" + in_account[-4:]
        logger.debug("Результат вычислен. Функция возвратила: %s", out_account_mask)
    else:
        out_account_mask = "данные не верны!"
        logger.error("Входные данные не число >=4 цифры. Функция возвратила: %s", out_account_mask)
    return out_account_mask
