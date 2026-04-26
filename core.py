import math
from collections import Counter
from .utils import ensure_list, is_numeric


class StatisticsError(ValueError):
    """Исключение для ошибок в статистических вычислениях."""
    pass


@validate_numeric
def mean(data):
    """Вычисляет среднее арифметическое за один проход."""
    data = list(data)  # Преобразуем в список для подсчета длины
    if not data:
        raise StatisticsError("Пустые данные.")
    return sum(data) / len(data)


@validate_numeric
def median(data):
    """Вычисляет медиану. Требует сортировки."""
    data_sorted = sorted(ensure_list(data))
    if not data_sorted:
        raise StatisticsError("Пустые данные.")

    n = len(data_sorted)
    mid = n // 2

    if n % 2 == 1:
        return data_sorted[mid]
    else:
        return (data_sorted[mid - 1] + data_sorted[mid]) / 2


@validate_numeric
def mode(data):
    """Вычисляет моду (наиболее часто встречающееся значение)."""
    data_list = ensure_list(data)
    if not data_list:
        raise StatisticsError("Пустые данные.")

    counter = Counter(data_list)
    max_count = max(counter.values())

    # Возвращаем первое встретившееся значение с максимальной частотой
    for value in data_list:
        if counter[value] == max_count:
            return value


@validate_numeric
def variance(data, ddof=0):
    """
    Вычисляет дисперсию по онлайн-алгоритму Велфорда за один проход.

    Args:
        data: Итератор чисел.
        ddof: Delta Degrees of Freedom. 0 для смещенной дисперсии, 1 для несмещенной.

    Raises:
        StatisticsError: Если данных недостаточно.
    """
    n = 0
    mean_ = 0.0
    M2 = 0.0  # Сумма квадратов отклонений

    for x in data:
        n += 1
        delta = x - mean_
        mean_ += delta / n
        M2 += delta * (x - mean_)

    if n == 0 or ddof >= n:
        raise StatisticsError("Недостаточно данных для вычисления дисперсии.")

    return M2 / (n - ddof)


@validate_numeric
def std(data, ddof=0):
    """Вычисляет стандартное отклонение как корень из дисперсии."""
    return math.sqrt(variance(data, ddof=ddof))