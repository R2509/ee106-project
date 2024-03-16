from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
import concurrent.futures
from pathlib import Path
from typing import Literal
import pandas as pd

from constants import (
    SENSOR_INDEX_MAX,
    SENSOR_INDEX_MIN,
    TIME_MAX,
    TIME_MIN,
)

from logger import logger


def sensor_text(index: int):
    '''Generates a sensor name from an index.'''
    return f"sensor_{str(index).rjust(2, '0')}"

def subset_df(
        df: pd.DataFrame,
        time_start: str = TIME_MIN,
        time_end: str = TIME_MAX,
        sensor_start: int = SENSOR_INDEX_MIN,
        sensor_end: int = SENSOR_INDEX_MAX,
        ):
    '''
    Select a subset of rows and columns in
    the dataframe. Based on a time range
    and a sensor range.
    '''

    # Change indexing column from default
    # (numeric index from CSV file) to
    # 'timestamp' column as we want to
    # index with time. (Solution found on StackOverflow)
    df.reset_index(inplace=True)
    df.set_index('timestamp', inplace=True)

    # Gather the requested cells into a nother DataFrame.
    check_param_excl = [
        time_start == TIME_MIN,
        time_end == TIME_MAX,
        sensor_start == SENSOR_INDEX_MIN,
        sensor_end == SENSOR_INDEX_MAX,
    ]
    if all(check_param_excl):
        cells = df
    else:
        # Integrate input validation
        cells = df.loc[
            time_start:time_end,
            sensor_text(sensor_start):sensor_text(sensor_end)
        ]

    # Convert DataFrame to a list of lists
    # Makes the data pickle-proof. It can
    # be parsed back into a Series or
    # DataFrame later when needed.
    return cells.values.tolist() #            <--| From supervisor
 
def data_summary(data: list | list[list]):
    '''
    Provide a data summary of the `Series` or `DataFrame` data provided.
    contains code suggested by supervisor.
    '''

    print('New process spawned...', flush=True)
    # Convert list, or list of lists, into
    # a Series or DataFrame respectively.
    if type(data[0]) == list:
        # If the list data is 2d (i.e. has nested
        # lists) it must represent a DataFrame.
        describable = pd.DataFrame(data)
    else:
        # The only other possible option is for
        # the data to represent a Series.
        describable = pd.Series(data)

    # Get Pandas to provide a summary on the
    # Series or DataFrame.
    desc = describable.describe()

    print('Process done.', flush=True)
    return desc

def map_data(data: list[list], method: int):
    '''
    Maps tasks over the passed `DataFrame`
    data, using the method specified.
    '''
    executor_class: type[Executor] = [
        ThreadPoolExecutor, #  | Method 0
        ProcessPoolExecutor, # | Method 1
    ][method]
    with executor_class() as executor:
        # Send individual columns, as well as
        # entire DataFrame subset.
        data_for_processes = [*data, data]
        descriptions = list(executor.map(data_summary, data_for_processes))
        executor.shutdown(wait=True)
    return descriptions

def summarise_file(
        file_path: str | Path,
        time_range: tuple[str, str] = (TIME_MIN, TIME_MAX),
        sensor_range: tuple[int, int] = (SENSOR_INDEX_MIN, SENSOR_INDEX_MAX),
        method: int = 0,
    ):
    '''
    Provide a data summary of the specified
    file, within the specified time and sensor
    range.
    '''
    df = logger.log_task(
        pd.read_csv,
        'Reading CSV data into DataFrame',
    )(file_path)

    data_subset = logger.log_task(
        subset_df,
        'Gathering DataFrame subset',
    )(df, *time_range, *sensor_range)

    mapped = logger.log_task(
        map_data,
        'Mapping tasks to processes',
    )(data_subset, method)

    return mapped
