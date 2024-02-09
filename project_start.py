'''
PARRALLEL PROCESSING ENGINE
'''

from pathlib import Path
import pandas as pd
from dataclasses import dataclass
dir_path = Path(__file__).parent.resolve()

## each function of pandas get an function to do a multithread processing thingy

# ClassName
# variable_or_function_name

class CSV:
    def __init__(self, csv_file_path: str | Path):
        self.dataframe: pd.DataFrame
        self._load_csv_into_df(csv_file_path)

    def _load_csv_into_df(self, csv_file_path):
        try:
            self.dataframe = pd.read_csv(csv_file_path)
        except Exception as exc:
            print('There was an error when loading the CSV file:')
            raise exc
        assert self.dataframe is not None, 'Fatal: empty dataframe. Exiting...'
    def _select_column(self, column_index: int):
        column_name = self.dataframe.columns[column_index]
        column_data = self.dataframe[column_name]
        return column_data

def open_csv():
    dataframe = pd.read_csv(dir_path / "sensor_timeseries.csv")
    column_name = dataframe.columns[2]
    print(dataframe[column_name].describe())

open_csv()



# def run_process_for_each_column()
#     pass


# def test():
#     for loop in range (100):
#         sleep(0.1)
#         print('hello')
  
# def test2():
#     for loop in range(100):
#         sleep(0.1)
#         print("ass")


# pr1 = mp.Process(target=test)
# pr2 = mp.Process(target=test2)
# pr2.start()
# pr1.start()
# pr2.join()
# pr1.join()

# print("th")




# def create_process_task():
#     if True: pass # REPLACE THIS WITH WHATEVER
