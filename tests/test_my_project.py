import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.my_project import triangle_type_and_coords


class TestTriangleType(unittest.TestCase):

    def test_equilateral_triangle(self):
        t_type, _ = triangle_type_and_coords(5, 5, 5)
        self.assertEqual(t_type, "равносторонний")

    def test_isosceles_triangle_two_equal_sides(self):
        t_type, _ = triangle_type_and_coords(5, 5, 8)
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene_triangle(self):
        t_type, _ = triangle_type_and_coords(3, 4, 5)
        self.assertEqual(t_type, "разносторонний")

    def test_not_triangle_sum_less_than_third(self):
        t_type, coords = triangle_type_and_coords(1, 2, 10)
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_triangle_zero_side(self):
        t_type, coords = triangle_type_and_coords(0, 5, 5)
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_not_triangle_negative_side(self):
        t_type, coords = triangle_type_and_coords(-3, 4, 5)
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_non_numeric_string(self):
        t_type, coords = triangle_type_and_coords("abc", "def", "ghi")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_string(self):
        t_type, coords = triangle_type_and_coords("", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_none_input(self):
        t_type, coords = triangle_type_and_coords(None, 4, 5)
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    # --- Бесконечность и NaN ---
    def test_infinity_input(self):
        t_type, coords = triangle_type_and_coords(float('inf'), 1, 1)
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_nan_input(self):
        t_type, coords = triangle_type_and_coords(float('nan'), 1, 1)
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_coords_length(self):
        _, coords = triangle_type_and_coords(3, 4, 5)
        self.assertEqual(len(coords), 3)

    def test_coords_are_integers(self):
        _, coords = triangle_type_and_coords(3, 4, 5)
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_coords_in_field(self):
        _, coords = triangle_type_and_coords(3, 4, 5)
        for x, y in coords:
            self.assertTrue(0 <= x <= 99)
            self.assertTrue(0 <= y <= 99)

    def test_coords_for_equal_sides(self):
        _, coords = triangle_type_and_coords(10, 10, 10)
        for x, y in coords:
            self.assertTrue(0 <= x <= 99)
            self.assertTrue(0 <= y <= 99)

    def test_string_numbers_converted(self):
        t_type, _ = triangle_type_and_coords("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")


if __name__ == "__main__":
    unittest.main()