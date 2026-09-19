import logging
import sys
import os

from lab1 import triangle_type_and_coords

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

os.makedirs("Logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8")
    ]
)


def Main():
    logging.info("=" * 60)
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    try:
        a = input("Введите длину стороны A: ").strip()
        b = input("Введите длину стороны B: ").strip()
        c = input("Введите длину стороны C: ").strip()

        logging.debug(f"Пользователь ввёл: a={a!r}, b={b!r}, c={c!r}")

        t_type, coords = triangle_type_and_coords(a, b, c)

        print()
        print("=" * 40)
        print(f"Тип треугольника: {t_type!r}")
        print(f"Координаты вершин: {coords}")
        print("=" * 40)

        logging.info(f"Результат: тип='{t_type}', координаты={coords}")

    except Exception as ex:
        logging.error("Что-то пошло не так...")
        logging.exception("Заход в блок обработки исключения:")
        print("Произошла непредвиденная ошибка. Подробности в логе.")

    finally:
        logging.info("Приложение завершено")
        logging.info("=" * 60)


if __name__ == "__main__":
    Main()