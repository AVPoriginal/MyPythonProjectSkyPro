import logging
import os
import pytest


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


if __name__ == "__main__":
    # настройка логирования
    setup_logging()
    print("Логирование сконфигурировано. Запуск pytest...")

    # запуск тестов
    pytest.main(["-s", "-v"])
