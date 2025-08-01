# from core.excel_processor import ExcelProcessor
#
# # Initialize the ExcelProcessor
# excel_processor = ExcelProcessor()
#
# # Define the file paths
# file_paths = [
#     r"D:\Intership Code generation\Assignment 2\financial-data-parser\data\sample\Customer_Ledger_Entries_FULL.xlsx",
#     r"D:\Intership Code generation\Assignment 2\financial-data-parser\data\sample\KH_Bank.XLSX"
# ]
#
# # Load the Excel files
# excel_processor.load_files(file_paths)
#
# # Get sheet information for both files
# for file_path in file_paths:
#     sheet_info = excel_processor.get_sheet_info()
#     print(f"Sheet Information for {file_path}:", sheet_info[file_path])
#
#     # Preview data from the first sheet of each file
#     first_sheet_name = list(sheet_info[file_path].keys())[0]
#     preview = excel_processor.preview_data(file_path, first_sheet_name)
#     print(f"Preview of Data from {first_sheet_name}:\n", preview)
#     print("\n" + "=" * 50 + "\n")  # Separator for clarity
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
