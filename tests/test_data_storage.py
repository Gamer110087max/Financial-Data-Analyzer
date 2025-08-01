import unittest
import pandas as pd
from core.data_storage import DataStorage

class TestDataStorage(unittest.TestCase):
    def setUp(self):
        self.storage = DataStorage()

    def test_store_data(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        self.storage.store_data('test_data', df, {'A': 'numeric', 'B': 'numeric'})
        self.assertIn('test_data', self.storage.data)
        self.assertEqual(self.storage.data['test_data'].shape, (2, 2))

    def test_create_indexes(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        self.storage.store_data('test_data', df, {'A': 'numeric', 'B': 'numeric'})
        self.storage.create_indexes('test_data')

        # Check if indexes were created
        self.assertIn(('test_data', 'A'), self.storage.indexes)
        self.assertIn(('test_data', 'B'), self.storage.indexes)

        # Check if the index lists are correct
        self.assertEqual(self.storage.indexes[('test_data', 'A')], [0, 1])  # Indexes for column A
        self.assertEqual(self.storage.indexes[('test_data', 'B')], [0, 1])  # Indexes for column B

    def test_aggregate_data(self):
        df = pd.DataFrame({'A': [1, 1, 2], 'B': [3, 4, 5]})
        self.storage.store_data('test_data', df, {'A': 'numeric', 'B': 'numeric'})
        result = self.storage.aggregate_data('A', ['sum'])

        # Ensure result is not None
        self.assertIsNotNone(result)

        # Check the aggregated result
        self.assertEqual(result.loc[result['A'] == 1, 'B'].values[0], 7)  # Check sum for group A=1
        self.assertEqual(result.loc[result['A'] == 2, 'B'].values[0], 5)  # Check sum for group A=2

    def test_aggregate_data(self):
        df = pd.DataFrame({'A': [1, 1, 2], 'B': [3, 4, 5]})
        self.storage.store_data('test_data', df, {'A': 'numeric', 'B': 'numeric'})
        result = self.storage.aggregate_data('A', ['sum'])

        # Ensure result is not None
        self.assertIsNotNone(result)

        # Check the aggregated result
        self.assertEqual(result.loc[result['A'] == 1, 'B'].values[0], 7)  # Check sum for group A=1
        self.assertEqual(result.loc[result['A'] == 2, 'B'].values[0], 5)  # Check sum for group A=2


if __name__ == '__main__':
    unittest.main()
