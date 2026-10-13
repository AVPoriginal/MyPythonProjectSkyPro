############################
# module for homework 11.2 #
############################
import time
import functools
import sys


def log(filename=None):
    """Декоратор для логирования времени выполнения, имени, результата или ошибки."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # если filename есть открываем файл
            # если filename пустой/None используем консоль
            out_target = open(filename, "a", encoding="UTF-8") if filename else sys.stdout
            # имя функции из метаданных для логирования
            func_name = func.__name__
            # время старта выполнения функции для логирования
            start_time = time.time()
            try:
                # выполняем функцию
                result = func(*args, **kwargs)
                # вычисляем время выполнения для логирования
                execution_time = time.time() - start_time
                # формируем запись в лог для успешного выполнения
                log_msg = (
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Функция: {func_name} | "
                    # f"Время выполнения: {execution_time:.4f} сек | "
                    f"Время выполнения: {execution_time} сек | "
                    f"Результат: {result}\n"
                )
            except Exception as e:
                # вычисляем время возникновения ошибки для логирования
                execution_time = time.time() - start_time
                # собираем входные параметры для лога ошибки
                inputs = f"args={args}, kwargs={kwargs}"
                # формируем запись в лог для случая ошибки
                log_msg = (
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"ОШИБКА в {func_name} | "
                    f"Тип ошибки: {type(e).__name__} ({e}) | "
                    f"Входные параметры: {inputs} | "
                    # f"Время до сбоя: {execution_time:.4f} сек\n"
                    f"Время до сбоя: {execution_time} сек\n"
                )
                # запись в лог и передаем ошибку если ошибка
                print(log_msg, file=out_target)
                raise e

            # запись в лог если выполнение
            print(log_msg, file=out_target)
            # закрываем открытый файл
            if filename:
                out_target.close()
            return result

        return wrapper

    return decorator
