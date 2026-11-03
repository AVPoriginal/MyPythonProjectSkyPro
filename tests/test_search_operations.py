
import pytest

from src.search_operations import process_bank_operations, process_bank_search


# фикстура с тестовыми данными
@pytest.fixture
def sample_data():
    return [
        {"id": 1, "description": "Перевод с карты на карту", "amount": 100},
        {"id": 2, "description": "Оплата услуг: Мобильная связь", "amount": 500},
        {"id": 3, "description": "Пополнение счета", "amount": 1000},
        {"id": 4, "description": "ПЕРЕВОД ОРГАНИЗАЦИИ", "amount": 5000},
        {"id": 5, "description": None, "amount": 0},  # тест на None
        {"id": 6},  # тест на отсутствие ключа description
        {"id": 7, "description": "Перевод с карты на карту"},

    ]

# тесты к process_bank_search


def test_search_successful_match(sample_data):
    """ тест на обычный успешный поиск подстроки """
    result = process_bank_search(sample_data, "связь")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_case_insensitive(sample_data):
    """ тест на проверку регистронезависимости (ищет 'перевод', находит 'Перевод' и 'ПЕРЕВОД') """
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 3
    assert {item["id"] for item in result} == {1, 4, 7}


def test_search_special_characters(sample_data):
    """тест на корректную обработку спецсимволов благодаря re.escape"""
    #  элемент со спецсимволом в описании
    data = [
        {"id": 10, "description": "Оплата услуг (ЖКХ) + комиссия"},
    ]
    # если re.escape работает то круглые скобки и плюс не сломают поиск
    result = process_bank_search(data, "(ЖКХ) +")
    assert len(result) == 1
    assert result[0]["id"] == 10


def test_search_no_results(sample_data):
    """ тест на поиск строки которой точно нет в данных """
    result = process_bank_search(sample_data, "Криптовалюта")
    assert result == []


def test_search_empty_query(sample_data):
    """ тест на пустую строку поиска должен находить всё с описанием включая пустую строку """
    result = process_bank_search(sample_data, "")
    assert len(result) == len(sample_data)


def test_search_empty_data():
    """ тест на пустой список данных """
    result = process_bank_search([], "перевод")
    assert result == []


def test_search_none_handling(sample_data):
    """тест на слово 'none' не должен находить пустые описания"""
    result = process_bank_search(sample_data, "none")
    assert result == []


# тесты к process_bank_operations


def test_successful_counting(sample_data):
    """тест на подсчет существующих категорий"""
    categories = ["Перевод с карты на карту", "Отация услуг", "Пополнение счета"]
    # Перевод с карты на карту — 2, Пополнение счета — 1, Отация услуг — 0 (опечатка в поиске)
    expected = {
        "Перевод с карты на карту": 2,
        "Отация услуг": 0,
        "Пополнение счета": 1
    }
    result = process_bank_operations(sample_data, categories)
    assert result == expected


def test_categories_order(sample_data):
    """тест на возврат ключей в словаре в том порядке в каком переданы категории"""
    categories = ["Пополнение счета", "Перевод с карты на карту"]
    result = process_bank_operations(sample_data, categories)
    assert list(result.keys()) == categories


def test_category_not_in_data(sample_data):
    """тест на отсутствие категории в операциях -должен вернуться 0"""
    categories = ["Покупка авиабилетов", "Штрафы ГИБДД"]
    expected = {"Покупка авиабилетов": 0, "Штрафы ГИБДД": 0}
    result = process_bank_operations(sample_data, categories)
    assert result == expected


def test_empty_inputs():
    """тест на обработку пустых списков на входе"""
    # если данных нет то для всех запрашиваемых категорий должен быть 0
    assert process_bank_operations([], ["Оплата услуг"]) == {"Оплата услуг": 0}
    # если список категорий пустой то должен вернуться пустой словарь
    assert process_bank_operations([{"description": "Тест"}], []) == {}


def test_none_and_missing_description_ignored(sample_data):
    """тест проверяет что элементы с None или отсутствующим ключом не вызывают ошибку"""
    # Counter посчитает их как None но если мы их не запрашиваем в categories они просто проигнорируются
    categories = ["Перевод с карты на карту"]
    result = process_bank_operations(sample_data, categories)
    assert result == {"Перевод с карты на карту": 2}
