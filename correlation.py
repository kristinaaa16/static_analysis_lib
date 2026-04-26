from .core import std


def covariance(x, y, ddof=1):
    x = list(x)
    y = list(y)
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("Длины последовательностей должны совпадать и быть ненулевыми.")
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n  # Используем среднее для стабильности
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - ddof)


def pearson_correlation(x, y):
    x = list(x)
    y = list(y)
    if len(x) != len(y):
        raise ValueError("Длины должны совпадать.")

    sx = std(x, ddof=0)
    sy = std(y, ddof=0)

    if sx == 0 or sy == 0:
        raise ValueError("Стандартное отклонение одной из выборок равно 0.")

    return covariance(x, y, ddof=1) / (sx * sy)