import pandas as pd


class ExcelProcessor:
    def __init__(self):
        self.data = {}
        self.sheet_info = {}

    def load_files(self, file_paths):
        for file_path in file_paths:
            xls = pd.ExcelFile(file_path)
            self.data[file_path] = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
            self.sheet_info[file_path] = {sheet: {'dimensions': self.data[file_path][sheet].shape,
                                                  'columns': self.data[file_path][sheet].columns.tolist()}
                                          for sheet in xls.sheet_names}

    def get_sheet_info(self):
        return self.sheet_info

    def extract_data(self, file_path, sheet_name):
        return self.data[file_path][sheet_name]

    def preview_data(self, file_path, sheet_name, rows=5):
        return self.data[file_path][sheet_name].head(rows)
