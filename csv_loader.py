'''
Definition of `CSVLoader` class.
'''

from pathlib import Path

from pandas import (
    DataFrame,
    Series,
    read_csv,
)
from pandas.api.types import (
    is_numeric_dtype,
)


class CSVManager:
    '''
    Manages the loading, storage and analysis of CSV data.

    ```py
    mgr = CSVManager('path/to/a/csv_file.csv')
    print(mgr.mean())
    ```
    '''

    def __init__(self, file_path: str | Path) -> None:
        '''
        Parameters:
        - `csv_path`: The path of the CSV file to load. This may
        be specified as a string or as a `pathlib.Path` object.
        '''
        self.df: DataFrame
        self._load_data(file_path)

    def _ensure_numeric(self, series: Series) -> None:
        '''
        Verifies that the passed `Series` object, `series`, contains only
        numeric data.
        
        Parameters:
        - `series`: The `Series` object to check

        Raises:
        - `TypeError` if `series` is not numeric.
        '''
        if not is_numeric_dtype(series):
            raise TypeError(
                f"The series must be numeric. The series '{series.name}' "
                f"has a dtype of '{series.dtype}', which is not numeric."
            )
    def _load_data(self, file_path: str | Path) -> None:
        '''
        Fetch the data from specified file and load it into instance.
        
        Parameters:
        - `csv_path`: The path of the CSV file to load. This may
        be specified as a string or as a `pathlib.Path` object.
        '''
        # Store in temporary variable to make debugging easier.
        # Will be removed for final version.
        dataframe = read_csv(file_path)

        # Assign value to instance variable
        self.df = dataframe
    def _get_column_by_name(self, column_name: str) -> Series:
        '''
        Retrieve data from the DataFrame column named `column_name`.

        Parameters:
        - `column_name`: The name of the column to retrieve data from.
        '''
        return self.df.loc[:, column_name]
    def describe_column(self, column_name: str) -> Series:
        '''
        ## CSVManager.describe_column

        Provide a statistical summary on the column whose name is `column_name`.
        The column data must be numeric.

        Uses `pandas.Series.describe()` to generate the summary.

        Parameters:
        - `column_name`: The name of the column to retrieve data from.
        '''
        column = self._get_column_by_name(column_name)
        self._ensure_numeric(column)
        return column.describe()
