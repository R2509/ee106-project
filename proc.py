from datetime import datetime
from pathlib import Path
from time import perf_counter

from pandas import DataFrame, Series, read_csv

from util import (
    logger,

    get_executor_class,

    TIME_MIN,
    TIME_MAX,
    SENSOR_INDEX_MIN,
    SENSOR_INDEX_MAX,
    subset_df,
)


def subprocess_task(data: list | list[list]):
    '''
    Provide a data summary of the `Series` or `DataFrame` data provided.
    contains code suggested by supervisor.
    '''

    # Convert list, or list of lists, into
    # a Series or DataFrame respectively.
    if type(data[0]) == list:
        # If the list data is 2d (i.e. has nested
        # lists) it must represent a DataFrame.
        describable = DataFrame(data)
    else:
        # The only other possible option is for
        # the data to represent a Series.
        describable = Series(data)

    # Get Pandas to provide a summary on the
    # Series or DataFrame.
    desc = describable.describe()

    return desc

def generate_descriptions(column_data: list[list], method: str):
    '''
    Maps tasks over the passed `DataFrame`
    data, using the method specified.
    '''
    executor_class = get_executor_class(method)

    with executor_class() as executor:
        # Record start time.
        start_time = perf_counter()

        # Send individual columns to subprocesses.
        descriptions = list(executor.map(subprocess_task, column_data))

        # **Wait for tasks** and shut down. From StackOverflow.
        executor.shutdown(wait=True)

        # Record execution duration.
        duration = perf_counter() - start_time

    return descriptions, duration


def summarise_file(
        file_path: str | Path,
        time_range: tuple[datetime, datetime] = (TIME_MIN, TIME_MAX),
        sensor_range: tuple[int, int] = (SENSOR_INDEX_MIN, SENSOR_INDEX_MAX),
        method: str = 'process',
    ):
    '''
    Provide a data summary of the specified
    file, within the specified time and sensor
    range.
    '''

    # Read the CSV file and store the contents in a Pandas DataFrame.
    df = logger.log_task('Reading CSV file data into DataFrame... ')\
        (read_csv)(file_path)

    # Create a subset of the dataset based on inputs.
    data_subset = logger.log_task('Creating DataFrame subset for analysis... ')\
        (subset_df)(df, *time_range, *sensor_range)

    # Get a summary of all the data.
    results = logger.log_task('Mapping analysis tasks to processes... ')\
        (generate_descriptions)(data_subset, method)

    return results
