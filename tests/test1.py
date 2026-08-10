# пример шаблона при создании файла теста из среды
# import unittest
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
# if __name__ == '__main__':
#     unittest.main()
# in_card_number = "1234567890123456"

# пример который найден и переделан из другого проекта
# test_unittest.py
import unittest
from src.masks import get_mask_card_number


class TestEven(unittest.TestCase):
    def test_is_even(self):
        cases = [
            ("1234567890123456", "1234 56** **** 3456"),
            ("12345678901234566", "данные не верны!"),
            ("1234567", "данные не верны!"),
            ("123456789012345A", "данные не верны!"),
        ]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(get_mask_card_number(number), expected)
