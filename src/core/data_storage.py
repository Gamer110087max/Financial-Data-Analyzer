class DataStorage:
    def __init__(self):
        self.data = {}
        self.indexes = {}
        self.metadata = {}

    def store_data(self, name, dataframe, column_types):
        self.data[name] = dataframe
        self.metadata[name] = column_types

    def create_indexes(self, name):
        # Check if the data exists
        if name in self.data:
            df = self.data[name]
            # Create indexes for all columns
            for column in df.columns:
                self.indexes[(name, column)] = df[column].index.tolist()  # Store the index of the column
        else:
            raise ValueError(f"No data found for {name}")

    def query_by_criteria(self, filters):
        # Check if the data exists
        if not self.data:
            return None

    def aggregate_data(self, group_by, measures):
        # Check if the data exists
        if not self.data:
            return None

        # Assuming we are aggregating the first stored DataFrame
        df = next(iter(self.data.values()))  # Get the first DataFrame

        # Perform aggregation
        if group_by in df.columns:
            if 'sum' in measures:
                return df.groupby(group_by).sum().reset_index()
            # You can add more aggregation methods here (e.g., mean, count, etc.)

        return None  # Return None if the group_by column is not found
