from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import pandas as pd
 
dirpath = Path(__file__).resolve().parent
 
def sensor_text(index: int):
    '''Generates a sensor name from an index.'''
    return f"sensor_{str(index).rjust(2, '0')}"
 
def df_select(df: pd.DataFrame, time_start: str, time_end: str, sensor_start: int, sensor_end: int):
    '''Select the rows and columns from the sensor dataframe.'''
    cells = df.loc[time_start:, sensor_text(sensor_start):sensor_text(sensor_end)]
    print(cells); exit()
    return cells.values.tolist() # Convert DataFrame to a list of lists
 
def data_summary(column: list):
    '''Provide a data summary of the column provided.'''
    return pd.Series(column).describe()
 
def main():
    '''Main function.'''
    df = pd.read_csv(dirpath / 'sensor_timeseries.csv')
    cols = df_select(df, '20180401', '20180402', 25, 50)
    with ProcessPoolExecutor() as executor:
        summaries = list(executor.map(data_summary, zip(*cols)))
        for summary in summaries:
            print(summary)
 
if __name__ == '__main__':
    main()