from collections import namedtuple
from .core import mean

# Определяем структуру модели с именованными полями для удобства чтения кода.
LinearRegressionModel = namedtuple('LinearRegressionModel',
                                   ['slope', 'intercept', 'r_squared', 'mse', 'predictions', 'residuals'])


def linear_regression(x, y):
    """
    Выполняет простую линейную регрессию методом наименьших квадратов.

    Returns:
        namedtuple с полями: slope, intercept, r_squared, mse, predictions, residuals.

    Raises:
        ValueError: Если длины не совпадают или данных мало.
    """

    x_list = list(x)
    y_list = list(y)

    if len(x_list) != len(y_list) or len(x_list) < 2:
        raise ValueError("Длины должны совпадать и быть не менее 2.")

    n = len(x_list)

    mx = mean(x_list)
    my = mean(y_list)

    # Вычисляем коэффициенты наклона (slope) и сдвига (intercept)

    # Числитель: сумма произведений отклонений (можно заменить на covariance(x,y)*n*(n-1))
    numerator = sum((xi - mx) * (yi - my) for xi, yi in zip(x_list, y_list))

    # Знаменатель: сумма квадратов отклонений x от среднего
    denominator = sum((xi - mx) ** 2 for xi in x_list)

    slope = numerator / denominator

    # Свободный член (intercept): b = y_mean - slope * x_mean
    intercept = my - slope * mx

    # Предсказанные значения y на основе модели y_hat = slope*x + intercept
    predictions = [slope * xi + intercept for xi in x_list]

    # Остатки (ошибки): разница между реальным и предсказанным значением
    residuals = [yi - y_pred for yi, y_pred in zip(y_list, predictions)]

    # Средняя квадратичная ошибка (MSE): среднее от квадратов остатков
    mse = sum(r ** 2 for r in residuals) / n

    # Коэффициент детерминации R^2: доля объясненной дисперсии.
    ss_res = sum(r ** 2 for r in residuals)  # Сумма квадратов остатков
    ss_tot = sum((yi - my) ** 2 for yi in y_list)  # Общая сумма квадратов отклонений от среднего y

    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0  # Если все y одинаковы, R^2 не определен (принимаем за 0)

    return LinearRegressionModel(slope=slope,
                                 intercept=intercept,
                                 r_squared=r_squared,
                                 mse=mse,
                                 predictions=predictions,
                                 residuals=residuals)


def predict(model, new_x):
    """
    Предсказывает значения на основе обученной модели.

    Args:
        model: Объект LinearRegressionModel.
        new_x: Число или итерируемый объект чисел.

    Returns:
        float или генератор предсказанных значений.

    Raises:
        TypeError: Если модель некорректна или new_x имеет неверный тип.
    """

    if not isinstance(model, LinearRegressionModel):
        raise TypeError("Модель некорректна.")

    def _predict_single(xi):
        return model.slope * xi + model.intercept

    if isinstance(new_x, (int, float)):
        return _predict_single(new_x)

    try:
        iter(new_x)
        return (_predict_single(xi) for xi in new_x)
    except TypeError:
        raise TypeError("new_x должен быть числом или итерируемым объектом чисел.")