import unittest
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    def test_normal_delivery_light_package(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", False)
        self.assertEqual(cost, 700)

    def test_normal_delivery_medium_package(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный", False)
        self.assertEqual(cost, 840)

    def test_normal_delivery_heavy_package(self):
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный", False)
        self.assertEqual(cost, 1700)

    def test_weight_exactly_5(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный", False)
        self.assertEqual(cost, 840)

    def test_weight_exactly_20(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    # --- Границы дистанции ---
    def test_distance_min(self):
        cost, _ = calculate_delivery_cost(2.0, 1, "обычный", False)
        self.assertEqual(cost, 205)

    def test_distance_max(self):
        cost, _ = calculate_delivery_cost(2.0, 5000, "обычный", False)
        self.assertEqual(cost, 25200)

    def test_distance_too_far(self):
        cost, date = calculate_delivery_cost(2.0, 5001, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_too_light(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный", False)
        self.assertEqual(cost, -1)

    def test_weight_too_heavy(self):
        cost, date = calculate_delivery_cost(51.0, 100, "обычный", False)
        self.assertEqual(cost, -1)

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(2.0, 100, "супер-пупер", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_express_cost(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", True)
        self.assertEqual(cost, 1050)

    def test_delivery_date_format(self):
        _, date = calculate_delivery_cost(2.0, 100, "обычный", False)
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")

    def test_delivery_date_days(self):
        _, date = calculate_delivery_cost(2.0, 100, "обычный", False)
        expected = (datetime.date(2026, 9, 3) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(date, expected)

    def test_express_delivery_days(self):
        _, date = calculate_delivery_cost(2.0, 500, "обычный", True)
        self.assertNotEqual(date, "2026-09-03")

    def test_fragile_heavy_express(self):
        cost, _ = calculate_delivery_cost(25.0, 1000, "хрупкий", True)
        self.assertEqual(cost, 4050)


if __name__ == "__main__":
    unittest.main()