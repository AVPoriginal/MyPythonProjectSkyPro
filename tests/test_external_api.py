
import pytest
import requests
from unittest.mock import Mock, patch
from src.external_api import get_amount_in_rub


#####
#1

def test_get_amount_in_rub_currency_rub():
    """тест транзакции в рублях - без запроса к API"""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"name": "руб.", "code": "RUB"}
        }
    }
    # подмена requests.get
    with patch("src.external_api.requests.get") as mock_get:
        result = get_amount_in_rub(transaction)

        assert result == 100.50
        # проверка что метод get не вызывался
        mock_get.assert_not_called()


#####
#2

def test_get_amount_in_rub_currency_usd():
    """ тест транзакции в USD с подменой успешного ответа API """
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        # mock-объект будет имитировать ответ сервера
        mock_response = Mock()
        mock_response.status_code = 200
        # имитация ответа Exchange Rates API
        mock_response.json.return_value = {
            "success": True,
            "result": 6900.00
        }
        # измененный requests.get будет возвращать этот mock_response
        mock_get.return_value = mock_response
        # вызов тестируемой функции
        result = get_amount_in_rub(transaction)

        assert result == 6900.00

        # проверка однократного requests.get
        mock_get.assert_called_once()
        # проверка с какими параметрами был вызван API
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["from"] == "USD"
        assert kwargs["params"]["amount"] == 100.0


#####
#3

def test_get_amount_in_rub_api_server_error():
    """ тест когда API возвращает HTTP-ошибку """
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")
        mock_get.return_value = mock_response
        with pytest.raises(RuntimeError) as exc_info:
            get_amount_in_rub(transaction)

        assert "Не удалось подключиться к API конвертации валют" in str(exc_info.value)


#####
#4

def test_get_amount_in_rub_api_success_false():
    """ тест когда API ответил со статусом 200 но в json пришло success: False """
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": {"code": 101, "type": "invalid_api_key"}
        }
        mock_get.return_value = mock_response
        with pytest.raises(RuntimeError) as exc_info:
            get_amount_in_rub(transaction)

        assert "Ошибка API при конвертации" in str(exc_info.value)


#####
#5

def test_get_amount_in_rub_network_timeout():
    """ тест сбоя соединения """
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")
        with pytest.raises(RuntimeError) as exc_info:
            get_amount_in_rub(transaction)

        assert "Не удалось подключиться к API конвертации валют" in str(exc_info.value)
