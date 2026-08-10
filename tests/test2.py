import unittest
from src.masks import get_mask_account


class TestEven(unittest.TestCase):
    def test_is_even(self):
        cases = [("1234567890123456", "**3456"), ("A345678901234566", "данные не верны!"), ("123", "данные не верны!")]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(get_mask_account(number), expected)
