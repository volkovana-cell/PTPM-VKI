import logging
import math


def triangle_type_and_coords(a, b, c):
    logging.debug(f"Входные данные: a={a!r}, b={b!r}, c={c!r}")

    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except (ValueError, TypeError) as ex:
        logging.error(f"Нечисловые данные: {ex}")
        logging.exception("Стек ошибки:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logging.warning(f"Стороны должны быть > 0: a={a}, b={b}, c={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if not (math.isfinite(a) and math.isfinite(b) and math.isfinite(c)):
        logging.warning(f"Обнаружены inf/nan: a={a}, b={b}, c={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning(f"Неравенство треугольника нарушено: {a}, {b}, {c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        t_type = "равносторонний"
    elif a == b or a == c or b == c:
        t_type = "равнобедренный"
    else:
        t_type = "разносторонний"

    logging.info(f"Тип треугольника определён: {t_type}")

    coords = _calculate_coords(a, b, c)
    logging.info(f"Координаты вершин: {coords}")
    return t_type, coords


def _calculate_coords(a, b, c):
    x = (a**2 + c**2 - b**2) / (2 * c)
    y = math.sqrt(max(0.0, a**2 - x**2))

    min_x, max_x = min(0, c, x), max(0, c, x)
    min_y, max_y = min(0, y), max(0, y)
    width, height = max_x - min_x, max_y - min_y

    max_dim = max(width, height)
    scale = 80.0 / max_dim if max_dim > 0 else 1.0

    offset_x = (100 - width * scale) / 2 - min_x * scale
    offset_y = (100 - height * scale) / 2 - min_y * scale

    def transform(px, py):
        tx = max(0, min(99, int(round(px * scale + offset_x))))
        ty = max(0, min(99, int(round(py * scale + offset_y))))
        return (tx, ty)

    return [transform(0, 0), transform(c, 0), transform(x, y)]