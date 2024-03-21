'''
Main processing functionality.
'''

from pathlib import Path
from time import perf_counter

from pandas import DataFrame, Series, read_csv

import logger
from util import (
    CLEAR_LINE,

    get_executor_class,

    TIME_MIN,
    TIME_MAX,
    SENSOR_INDEX_MIN,
    SENSOR_INDEX_MAX,
    COLUMN_WIDTH,
    get_summaries_per_df,
    sensor_name,
    subset_df,
)


def subprocess_task(data: list):
    '''
    Provide a data summary of the `Series` or `DataFrame` data provided.
    contains code suggested by supervisor.
    '''

    # Get Pandas to provide a summary on the Series data.
    desc = Series(data).describe()

    return desc

def generate_descriptions(columns: list[list], method: str):
    '''
    Maps tasks over the passed `DataFrame`
    data, using the method specified.
    '''
    executor_class = get_executor_class(method)

    # Record start time.
    start_time = perf_counter()
    if executor_class is None:
        # Perform task synchronously.
        descriptions = [subprocess_task(column) for column in columns]
    else:
        # Perform task using multiprocessing or multithreading.
        with executor_class() as executor:

            # Send individual columns to subprocesses.
            descriptions = list(executor.map(subprocess_task, columns))

            # **Wait for tasks** and shut down. From StackOverflow.
            executor.shutdown(wait=True)

    # Record execution duration.
    duration = perf_counter() - start_time

    return descriptions, duration

def collate_results(
        results: list[Series],
        sensor_start: int,
        sensor_end: int,
        entries_per_df: int,
    ):
    '''
    Generate a `DataFrame` containing descriptions of all selected columns.
    '''

    # generate a list of sensor names. Will be used as
    # column headings in the DataFrame.
    # TODO: document this stuff better...
    sensor_range = [
        sensor_name(index).rjust(COLUMN_WIDTH - 2, chr(160))
        for index in range(sensor_start, sensor_end + 1)
    ]

    # Generate entries which a dict can be constructed
    # from. Will provide data for DataFrame.
    dict_entries = [
        (sensor_range[index], results[index])
        for index in range(len(results))
    ]

    # Create a DataFrame using a dict generated from the entried above.
    dataframes = [
        DataFrame({ k: v for k, v in dict_entries[entry_group_start:entry_group_start + entries_per_df]})
        for entry_group_start in range(0, len(results), entries_per_df)
    ]

    # Return the DataFrame.
    return dataframes


def summarise_file(
        file_path: str | Path,
        time_range: tuple[str, str] = (TIME_MIN, TIME_MAX),
        sensor_range: tuple[int, int] = (SENSOR_INDEX_MIN, SENSOR_INDEX_MAX),
        method: str = 'process',
        entries_per_df: int = get_summaries_per_df()
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
    series_data, time_taken = logger.log_task('Running analysis tasks... ')\
        (generate_descriptions)(data_subset, method)
    
    # Collate all results
    results = logger.log_task('Collating results... ')\
        (collate_results)(series_data, *sensor_range, entries_per_df)

    return results, time_taken

def benchmark(
        file_path: str | Path,
        time_range: tuple[str, str] = (TIME_MIN, TIME_MAX),
        sensor_range: tuple[int, int] = (SENSOR_INDEX_MIN, SENSOR_INDEX_MAX),
        method: str = 'process',
        times: int = 10,
    ):
    '''
    Provide a data summary of the specified file a specified number of times,
    within the specified time and sensor range.

    For benchmarking purposes. Does not return results. If this is desired, use
    summarise_file() instead.
    '''

    # Read the CSV file and store the contents in a Pandas DataFrame.
    df = logger.log_task('Reading CSV file data into DataFrame... ')\
        (read_csv)(file_path)

    # Create a subset of the dataset based on inputs.
    data_subset = logger.log_task('Creating DataFrame subset for analysis... ')\
        (subset_df)(df, *time_range, *sensor_range)

    # Add another timing counter so that the delays from printing can be minimsed
    printing_timer = -1
    threshold = 0.25

    # Run analysis a set number of times, as specified by `times`.
    # Record start time externally, and create list for internal times.
    start_time = perf_counter()
    internal_times: list[float] = []

    for index in range(times):
        if any([
            printing_timer > threshold,
            printing_timer == -1,
            times == index + 1,
        ]):
            logger.log(f'{CLEAR_LINE}Benchmarking analysis program... (run {index + 1} of {times})')
            printing_timer = 0
        _, time_taken = generate_descriptions(data_subset, method)
        printing_timer += time_taken
        # Record each internal time.
        internal_times.append(time_taken)
    # Store duration of entire execution.
    total_external_duration = perf_counter() - start_time
    total_internal_duration = sum(internal_times)

    # Gather benchmark timing results and provide a summary
    # of these.
    bench_results = logger.log_task('\nGathering benchmarking results... ')\
        (Series(internal_times).describe)()

    # Return all results.
    return bench_results, total_internal_duration, total_external_duration
