import pytest

from src.decorators import log


def test_log_to_console_success(capsys):
    """Тестируем успешное выполнение с выводом в консоль."""

    # тестовая функция
    @log(filename=None)
    def amount(x, y):
        return x + y

    result = amount(1, 2)
    # проверяем результат работы функции
    assert result == 3
    # перехватываем вывод в консоль
    captured = capsys.readouterr()
    # проверяем вывод на содержание
    assert "Функция: amount" in captured.out
    assert "Результат: 3" in captured.out
    assert "Время выполнения:" in captured.out


def test_log_to_console_error(capsys):
    """Тестируем падение функции с выводом ошибки в консоль."""

    # тестовая функция с гарантированной ошибкой
    @log(filename=None)
    def function_bad(a):
        return a / 0

    # проверяем что декоратор пробрасывает ошибку дальше
    with pytest.raises(ZeroDivisionError):
        function_bad(4)
    # проверяем что лог ошибки записался в консоль
    captured = capsys.readouterr()
    assert "ОШИБКА в function_bad" in captured.out
    assert "Тип ошибки: ZeroDivisionError" in captured.out
    assert "Входные параметры: args=(4,)" in captured.out
    assert "Время до сбоя:" in captured.out


def test_log_to_file_success(tmp_path):
    """Тестируем успешное выполнение с записью во временный файл."""
    # создаем путь к временному файлу который удалится после теста
    log_file = tmp_path / "test_success.log"

    # тестовая функция
    @log(filename=str(log_file))
    def multiplication(x, y):
        return x * y

    result = multiplication(3, 4)
    # проверяем результат работы функции
    assert result == 12
    # проверяем содержимое файла
    log_content = log_file.read_text(encoding="UTF-8")
    assert "Функция: multiplication" in log_content
    assert "Результат: 12" in log_content
    assert "Время выполнения:" in log_content


def test_log_to_file_error(tmp_path):
    """Тестируем запись ошибки во временный файл."""
    log_file = tmp_path / "test_error.log"

    # тестовая функция с гарантированной ошибкой
    @log(filename=str(log_file))
    def division_error():
        return 2 / 0

    with pytest.raises(ZeroDivisionError):
        division_error()

    # проверяем содержимое файла на наличие ошибки
    log_content = log_file.read_text(encoding="UTF-8")
    assert "ОШИБКА в division_error" in log_content
    assert "Тип ошибки: ZeroDivisionError" in log_content
    assert "Время до сбоя:" in log_content
    assert "Входные параметры: args=()" in log_content
