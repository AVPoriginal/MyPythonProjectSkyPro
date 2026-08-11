from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(in_account_card: str) -> str:
    """
    Принимает строку, содержащую тип и номер карты или счета
    Возвращает строку с замаскированным номером
    """

    # Превращаем строку в список полей
    account_string_fields = in_account_card.split()

    # Проверка на количество полей данных 2 или 3
    if len(account_string_fields) < 2 or len(account_string_fields) > 3:
        account_masked_number = "данные не верны"
        return account_masked_number

    # Выделение поля предполагаемого номера
    account_number_field = account_string_fields[(len(account_string_fields) - 1)]

    # проверка наличия корректного номера
    if len(account_number_field) < 4 or not account_number_field.isdigit():
        account_masked_number = "данные не верны"
        return account_masked_number

    # Проверка номер счета или номер карты и формирование маски
    if account_string_fields[0] == "Счет":
        account_masked_number = account_string_fields[0] + " " + get_mask_account(account_number_field)
        return account_masked_number

    if len(account_number_field) == 16:
        # account_masked_number = get_mask_card_number(account_number_field)
        account_string_fields[(len(account_string_fields) - 1)] = get_mask_card_number(account_number_field)
        account_masked_number = " ".join(account_string_fields)
        return account_masked_number
    else:
        account_masked_number = "данные не верны"
        return account_masked_number


# для быстрой проверки выполнения
# print(mask_account_card("Visa Platinum Счет 1234567890123456"))


def get_date(iso_string: str) -> str | None:
    try:
        d_m_y_format = datetime.fromisoformat(iso_string)
        return d_m_y_format.strftime("%d.%m.%Y")
    except ValueError:
        return None


# для быстрой проверки функции
# print(get_date("2024-03-11T02:26:18.671407"))
