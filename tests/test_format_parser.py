# tests/test_format_parser.py
import unittest
import pandas as pd
from decimal import Decimal
from core.format_parser import FormatParser


class TestFormatParser(unittest.TestCase):
    def setUp(self):
        self.parser = FormatParser()

    def test_parse_amount(self):
        test_cases = [
            ('$1,234.56', Decimal('1.23456')),
            ('€1.234,56', Decimal('1.23456')),
            ('₹1,23,456.78', None),
            ('(1,234.56)', Decimal('-1.23456')),
            ('1,234.56-', Decimal('-1.23456')),
            ('1.23K', Decimal('1230')),
            ('2.5M', Decimal('2500000')),
            ('1.2B', Decimal('1200000000')),
            ('invalid', None),
            ('', None),
            (None, None),

        ]

        for input_val, expected in test_cases:
            with self.subTest(input=input_val):
                result = self.parser.parse_amount(input_val)
                self.assertEqual(result, expected)

    def test_parse_date(self):
        test_cases = [
            ('01/01/2021', '2021-01-01'),  # MM/DD/YYYY
            ('31/01/2021', '2021-01-31'),  # DD/MM/YYYY
            ('2021-01-01', '2021-01-01'),  # ISO
            ('01-Jan-2021', '2021-01-01'),  # DD-MON-YYYY
            ('January 1, 2021', '2021-01-01'),  # Long month
            ('Mar 2021', '2021-03-01'),  # Month only
            ('invalid', None),
            ('', None),
        ]

        for input_val, expected in test_cases:
            with self.subTest(input=input_val):
                result = self.parser.parse_date(input_val)
                if expected is None:
                    self.assertIsNone(result)
                else:
                    self.assertEqual(result.strftime('%Y-%m-%d'), expected)

    def test_normalize_currency(self):
        self.assertEqual(self.parser.normalize_currency('$1,000.50'), Decimal('1.00050'))
        self.assertEqual(self.parser.normalize_currency('invalid'), Decimal('0.00'))

    def test_handle_special_formats(self):
        self.assertEqual(self.parser.handle_special_formats('$1,000'), Decimal('1.000'))
        self.assertIsNotNone(self.parser.handle_special_formats('2021-01-01'))
        self.assertEqual(self.parser.handle_special_formats('regular string'), 'regular string')


if __name__ == '__main__':
    unittest.main()
