# src/core/format_parser.py
import re
from datetime import datetime
import pandas as pd
from decimal import Decimal


class FormatParser:
    def parse_amount(self, value):
        if pd.isna(value) or value == '':
            return None

        original = str(value).strip()

        # Handle parentheses and trailing - for negatives
        is_negative = False
        if '(' in original or original.endswith('-'):
            is_negative = True
            original = original.replace('(', '').replace(')', '').replace('-', '').strip()

        # Handle abbreviations (K, M, B)
        abbrev = {'K': 1e3, 'M': 1e6, 'B': 1e9}
        for unit, multiplier in abbrev.items():
            if unit in original:
                num = re.sub(r'[^\d\.]', '', original.replace(unit, ''))
                return Decimal(float(num) * multiplier * (-1 if is_negative else 1))

        # Standard number parsing
        num_str = re.sub(r'[^\d\.,-]', '', original)

        # European vs. US decimal separation
        if ',' in num_str and '.' in num_str:
            if num_str.find(',') < num_str.find('.'):  # 1.234,56 format
                num_str = num_str.replace('.', '').replace(',', '.')
            else:  # 1,234.56 format
                num_str = num_str.replace(',', '')
        elif ',' in num_str:  # European style with just comma
            num_str = num_str.replace(',', '.')

        try:
            return Decimal(num_str) * (-1 if is_negative else 1)
        except:
            return None

    def parse_date(self, value):
        if pd.isna(value) or value == '':
            return None

        # Excel serial dates
        if isinstance(value, (int, float)):
            try:
                return pd.to_datetime('1899-12-30') + pd.Timedelta(days=float(value))
            except:
                return None

        # Common date patterns
        date_formats = [
            '%m/%d/%Y',  # MM/DD/YYYY
            '%d/%m/%Y',  # DD/MM/YYYY
            '%Y-%m-%d',  # ISO format
            '%d-%b-%Y',  # DD-MON-YYYY (e.g., 01-Jan-2023)
            '%B %d, %Y',  # Month DD, YYYY
            '%b %d, %Y',  # Mon DD, YYYY
            '%b %Y',  # Mon YYYY
            '%B %Y',  # Month YYYY
            'Q%q %Y',  # Quarter
            'Q%q-%y',  # Quarter-ShortYear
        ]

        for fmt in date_formats:
            try:
                return pd.to_datetime(str(value), format=fmt, exact=True)
            except ValueError:
                continue

        return None

    def normalize_currency(self, value):
        """Convert all currency values to Decimal"""
        parsed = self.parse_amount(value)
        return parsed if parsed is not None else Decimal('0.00')

    def handle_special_formats(self, value):
        """Handle any special or custom formats"""
        # Try all parsing methods
        result = self.parse_date(value)
        if result is not None:
            return result

        result = self.parse_amount(value)
        if result is not None:
            return result

        return str(value).strip()
