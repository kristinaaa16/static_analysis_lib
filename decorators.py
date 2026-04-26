import functools
import time
import logging
from collections import OrderedDict
from .utils import is_numeric

def timer(func):
    """Декоратор: выводит время выполнения функции."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMER] {func.__name__} выполнена за {end - start:.6f} сек.")
        return result
    return wrapper

def logger(func):
    """Декоратор: логирует имя функции, аргументы и результат."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Вызов {func.__name__} с args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} вернула: {result}")
        return result
    return wrapper

def validate_numeric(func):
    """Декоратор: проверяет, что все элементы коллекций-аргументов являются числами."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, (list, tuple)):
                for item in arg:
                    if not is_numeric(item):
                        raise TypeError(f"Некорректный тип данных: {type(item)}. Ожидается int или float.")
            # Проверка одиночных аргументов (например, k в detect_outliers_iqr)
            elif is_numeric(arg) is False and arg is not None:
                raise TypeError(f"Некорректный тип аргумента: {type(arg)}")
        return func(*args, **kwargs)
    return wrapper

def memoize(maxsize=None):
    """Декоратор: кеширует результаты функции (LRU)."""
    def decorator(func):
        cache = OrderedDict()
        @functools.wraps(func)
        def wrapper(*args):
            if args in cache:
                # Перемещаем в конец, чтобы отметить как недавно использованный
                cache.move_to_end(args)
                return cache[args]
            result = func(*args)
            cache[args] = result
            if maxsize and len(cache) > maxsize:
                cache.popitem(last=False) # Удаляем самый старый элемент
            return result
        return wrapper
    return decorator