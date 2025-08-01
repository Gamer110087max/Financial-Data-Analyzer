import pandas as pd
import openpyxl
import numpy as np
import sqlite3
import re
from datetime import datetime
from decimal import Decimal
import locale
from core.excel_processor import ExcelProcessor
from core.type_detector import DataTypeDetector
from core.format_parser import FormatParser
from core.data_storage import DataStorage

# Initialize processors
excel_processor = ExcelProcessor()
data_type_detector = DataTypeDetector()
format_parser = FormatParser()
data_storage = DataStorage()

# Load the Excel files
file_paths = [
    r"D:\Intership Code generation\Assignment 2\financial-data-parser\data\sample\Customer_Ledger_Entries_FULL.xlsx",
    r"D:\Intership Code generation\Assignment 2\financial-data-parser\data\sample\KH_Bank.XLSX"
]
excel_processor.load_files(file_paths)

# Process each file
for file_path in file_paths:
    sheet_info = excel_processor.get_sheet_info()
    for sheet_name in sheet_info[file_path].keys():
        data = excel_processor.extract_data(file_path, sheet_name)
        column_types = {col: data_type_detector.analyze_column(data[col]) for col in data.columns}
        data_storage.store_data(sheet_name, data, column_types)
        print(f"Stored data for {sheet_name} with types: {column_types}")
