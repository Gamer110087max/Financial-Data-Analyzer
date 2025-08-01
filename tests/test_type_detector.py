import unittest
import pandas as pd
from core.type_detector import DataTypeDetector

class TestDataTypeDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DataTypeDetector()

    def test_analyze_column_numeric(self):
        data = pd.Series([1, 2, 3])
        result = self.detector.analyze_column(data)
        self.assertEqual(result, 'numeric')

    def test_analyze_column_datetime(self):
        data = pd.Series(pd.to_datetime(['2021-01-01', '2021-01-02']))
        result = self.detector.analyze_column(data)
        self.assertEqual(result, 'datetime')

    def test_analyze_column_string(self):
        data = pd.Series(['a', 'b', 'c'])
        result = self.detector.analyze_column(data)
        self.assertEqual(result, 'string')

    def test_analyze_column_unknown(self):
        data = pd.Series([None, None])
        result = self.detector.analyze_column(data)
        self.assertEqual(result, 'unknown')

if __name__ == '__main__':
    unittest.main()
