import unittest
import pandas as pd
from core.excel_processor import ExcelProcessor

class TestExcelProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ExcelProcessor()
        self.file_paths = [
            r"D:\Intership Code generation\Assignment 2\financial-data-parser\data\sample\Customer_Ledger_Entries_FULL.xlsx",
            r"D:\Intership Code generation\Assignment 2\financial-data-parser\data\sample\KH_Bank.XLSX"
        ]
        self.processor.load_files(self.file_paths)

    def test_load_files(self):
        # Check if files are loaded correctly
        self.assertIn(self.file_paths[0], self.processor.data)
        self.assertIn(self.file_paths[1], self.processor.data)

    def test_get_sheet_info(self):
        # Check if sheet information is retrieved correctly
        sheet_info = self.processor.get_sheet_info()
        self.assertIn(self.file_paths[0], sheet_info)
        self.assertIn(self.file_paths[1], sheet_info)

        # Check if the sheet names are present
        self.assertTrue(len(sheet_info[self.file_paths[0]]) > 0)
        self.assertTrue(len(sheet_info[self.file_paths[1]]) > 0)

    def test_extract_data(self):
        # Check if data can be extracted from a specific sheet
        first_sheet_name = list(self.processor.get_sheet_info()[self.file_paths[0]].keys())[0]
        data = self.processor.extract_data(self.file_paths[0], first_sheet_name)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(data.shape[0], 0)  # Ensure there is data in the DataFrame

    def test_preview_data(self):
        # Check if preview data returns the correct number of rows
        first_sheet_name = list(self.processor.get_sheet_info()[self.file_paths[0]].keys())[0]
        preview = self.processor.preview_data(self.file_paths[0], first_sheet_name, rows=5)
        self.assertEqual(preview.shape[0], 5)  # Ensure it returns 5 rows

if __name__ == '__main__':
    unittest.main()
