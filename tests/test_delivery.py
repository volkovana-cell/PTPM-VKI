import unittest
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    # --- Базовые сценарии ---
    def test_normal_delivery_light_package(self):
        """Обычная посылка до 5 кг."""
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", False)
        # 200 + 100*5 = 700
        self.assertEqual(cost, 700)

    def test_normal_delivery_medium_package(self):
        """Посылка 5-20 кг — коэффициент 1.2."""
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный", False)
        # (200 + 500) * 1.2 = 840
        self.assertEqual(cost, 840)

    def test_normal_delivery_heavy_package(self):
        """Посылка >= 20 кг — коэффициент 1.5."""
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный", False)
        # (200 + 500) * 1.5 = 1050
        self.assertEqual(cost, 1050)

    # --- Типы посылок ---
    def test_fragile_package_adds_300(self):
        """Хрупкая посылка — +300."""
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)  # 700 + 300

    def test_dangerous_package_adds_1000(self):
        """Опасная посылка — +1000."""
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный", False)
        self.assertEqual(cost, 1700)  # 700 + 1000

    # --- Границы веса ---
    def test_weight_exactly_5(self):
        """Ровно 5 кг — коэффициент НЕ применяется (БАГ)."""
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный", False)
        # Ожидаем 840 (с коэффициентом 1.2), но получим 700 из-за бага
        self.assertEqual(cost, 840)  # ⚠️ УПАДЁТ — это баг №1

    def test_weight_exactly_20(self):
        """Ровно 20 кг — коэффициент 1.5."""
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    # --- Границы дистанции ---
    def test_distance_min(self):
        """Минимальная дистанция 1 км."""
        cost, _ = calculate_delivery_cost(2.0, 1, "обычный", False)
        self.assertEqual(cost, 205)

    def test_distance_max(self):
        """Максимальная дистанция 5000 км."""
        cost, _ = calculate_delivery_cost(2.0, 5000, "обычный", False)
        self.assertEqual(cost, 25200)

    def test_distance_too_far(self):
        """Дистанция > 5000 — ошибка."""
        cost, date = calculate_delivery_cost(2.0, 5001, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # --- Границы веса ---
    def test_weight_too_light(self):
        """Вес < 0.1 — ошибка."""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный", False)
        self.assertEqual(cost, -1)

    def test_weight_too_heavy(self):
        """Вес > 50 — ошибка."""
        cost, date = calculate_delivery_cost(51.0, 100, "обычный", False)
        self.assertEqual(cost, -1)

    # --- Неверный тип посылки ---
    def test_invalid_package_type(self):
        """Несуществующий тип посылки — ошибка."""
        cost, date = calculate_delivery_cost(2.0, 100, "супер-пупер", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # --- Express ---
    def test_express_cost(self):
        """Express умножает стоимость на 0.5 (БАГ)."""
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", True)
        # Логично ожидать 1050 (дороже), но получим 350 (дешевле)
        self.assertEqual(cost, 1050)  # ⚠️ УПАДЁТ — это баг №2

    # --- Дата доставки ---
    def test_delivery_date_format(self):
        """Дата в формате YYYY-MM-DD."""
        _, date = calculate_delivery_cost(2.0, 100, "обычный", False)
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")

    def test_delivery_date_days(self):
        """100 км → 1 день (100 // 500 = 0 → max(1,0)=1)."""
        _, date = calculate_delivery_cost(2.0, 100, "обычный", False)
        expected = (datetime.date(2026, 9, 3) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(date, expected)

    def test_express_delivery_days(self):
        """Express: 500 км → 1 день, потом // 2 = 0 (БАГ)."""
        _, date = calculate_delivery_cost(2.0, 500, "обычный", True)
        # Ожидаем минимум 1 день, но получим 0
        self.assertNotEqual(date, "2026-09-03")  # ⚠️ УПАДЁТ — это баг №3

    # --- Комбинации ---
    def test_fragile_heavy_express(self):
        """Хрупкая + тяжёлая + express."""
        cost, _ = calculate_delivery_cost(25.0, 1000, "хрупкий", True)
        # (200 + 5000) * 1.5 + 300 = 7800 + 300 = 8100
        # Но express *0.5 → 4050
        self.assertEqual(cost, 4050)  # ⚠️ Это баг: должно быть дороже


if __name__ == "__main__":
    unittest.main()