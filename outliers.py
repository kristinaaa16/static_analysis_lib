from .core import median
from .decorators import validate_numeric
from .utils import ensure_list


class StatisticsError(ValueError):
    pass


def _calculate_iqr_bounds(data_sorted, k):
    """Вспомогательная функция для расчета границ IQR."""
    if len(data_sorted) < 4:
        raise StatisticsError("Недостаточно данных для вычисления квартилей.")

    # Находим индексы для разделения на четверти
    mid = len(data_sorted) // 2

    # Q1 - медиана первой половины, Q3 - медиана второй половины
    q1 = median(data_sorted[:mid])
    q3 = median(data_sorted[mid:]) if len(data_sorted) % 2 == 0 else median(data_sorted[mid + 1:])

    iqr = q3 - q1
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr

    return lower_bound, upper_bound


@validate_numeric
def detect_outliers_iqr(data, k=1.5):
    """
    Находит выбросы по методу межквартильного размаха (IQR).

    Returns:
        Список индексов выбросов в ИСХОДНОМ списке данных.

    Raises:
        StatisticsError: Если данных недостаточно.
    """
    # Создаем список пар (индекс, значение), чтобы не потерять исходные позиции
    indexed_data = list(enumerate(ensure_list(data)))

    # Сортируем пары по значению, чтобы корректно вычислить квантили
    sorted_indexed_data = sorted(indexed_data, key=lambda pair: pair[1])

    # Извлекаем только отсортированные значения для расчета границ
    sorted_values = [value for _, value in sorted_indexed_data]

    try:
        lower_bound, upper_bound = _calculate_iqr_bounds(sorted_values, k)
    except StatisticsError as e:
        raise e

    # Находим индексы выбросов в ОТСОРТИРОВАННОМ списке
    outlier_indices_in_sorted = [
        i for i, (_, x) in enumerate(sorted_indexed_data)
        if x < lower_bound or x > upper_bound
    ]

    # Извлекаем исходные индексы из пар (индекс, значение)
    original_indices = [sorted_indexed_data[i][0] for i in outlier_indices_in_sorted]

    return original_indices


def validate_numeric(args):
    pass


@validate_numeric
def remove_outliers(data, method='iqr', **kwargs):
    """
    Удаляет выбросы из данных.

    Returns:
        Генератор элементов без выбросов в ИСХОДНОМ порядке.

    Raises:
        ValueError: Если метод не поддерживается.
        StatisticsError: Если метод IQR не смог вычислить границы.
    """
    if method != 'iqr':
        raise ValueError(f"Метод '{method}' не поддерживается.")

    data_list = ensure_list(data)

    try:
        # Получаем индексы выбросов в исходном списке
        outlier_indices = detect_outliers_iqr(data_list, **kwargs)
    except StatisticsError as e:
        raise e

    # Создаем множество индексов для быстрого поиска
    outlier_indices_set = set(outlier_indices)

    # Генерируем элементы, индексы которых НЕ входят в список выбросов
    return (x for i, x in enumerate(data_list) if i not in outlier_indices_set)