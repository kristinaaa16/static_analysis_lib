import warnings
from collections.abc import Iterator

def is_numeric(value):
    """
    Проверяет, является ли значение числом (int или float), исключая bool.
    """
    return isinstance(value, (int, float)) and not isinstance(value, bool)

def ensure_list(iterable):
    """
    Преобразует итерируемый объект в список.
    Если на вход подается итератор (генератор), выводит предупреждение,
    так как это может привести к загрузке всех данных в память.
    """
    if isinstance(iterable, Iterator):
        warnings.warn("Преобразование итератора в список может привести к загрузке всех данных в память.")
    return list(iterable)