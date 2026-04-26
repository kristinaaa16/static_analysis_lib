import re
from decorators import validate_numeric


# ... (другие функции: read_numbers_from_file, sliding_window, streaming_mean, streaming_variance)

@validate_numeric
def streaming_pearson(x_iter, y_iter):
    """
    Потоковое вычисление коэффициента корреляции Пирсона.

    Returns:
        Генератор, выдающий текущий коэффициент корреляции Пирсона
        после каждой новой пары (x, y). До получения двух пар возвращает None.

    Note:
        Использует онлайн-алгоритм для численной устойчивости.
    """
    # Инициализируем итераторы и накопители сумм
    sum_x = sum_y = sum_xy = sum_x2 = sum_y2 = 0.0
    n = 0

    # Используем zip для попарного прохода по итераторам
    for x, y in zip(x_iter, y_iter):
        n += 1

        # Накапливаем суммы
        sum_x += x
        sum_y += y
        sum_xy += x * y
        sum_x2 += x * x
        sum_y2 += y * y

        # Для первой точки корреляция не определена
        if n == 1:
            yield None
            continue

        # Вычисляем ковариацию и стандартные отклонения по формулам
        # Ковариация: E[XY] - E[X]E[Y]
        covariance = (sum_xy / n) - (sum_x / n) * (sum_y / n)

        # Дисперсии: E[X^2] - (E[X])^2
        var_x = (sum_x2 / n) - (sum_x / n) ** 2
        var_y = (sum_y2 / n) - (sum_y / n) ** 2

        # Проверка на нулевую дисперсию, чтобы избежать деления на ноль
        if var_x <= 0 or var_y <= 0:
            yield 0.0
            continue

        # Вычисляем коэффициент корреляции Пирсона
        std_x = var_x ** 0.5
        std_y = var_y ** 0.5

        pearson_r = covariance / (std_x * std_y)

        # Гарантируем, что результат не выходит за пределы [-1, 1] из-за погрешностей вычислений
        yield max(min(pearson_r, 1.0), -1.0)