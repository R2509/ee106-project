'''
Contains general utilities used throughout the program.
'''

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
from shutil import get_terminal_size
import sys
from typing import Any, Callable
from pandas import DataFrame


# Minimum and maximum values for measurement time.
TIME_MIN = '2018-04-01 00:00:00'
TIME_MAX = '2018-08-31 23:59:00'

# Minimum and maximum values for sernsor index.
SENSOR_INDEX_MIN = 0
SENSOR_INDEX_MAX = 51

# Text formatting escape codes
CLEAR_LINE = '\x1b[2K\x1b[G'
CLEAR_SCREEN = '\x1b[2J\x1b[H'
TEXT_RESET = '\x1b[m'
TEXT_GREY = '\x1b[38;5;245m'

# Column width used in formatting results.
# MINIMUM VALUE: 15
COLUMN_WIDTH = 16


def sensor_name(index: int):
    '''
    Generates a sensor name from an index.
    '''
    # Use an f-string to generate the name of the sensor.
    return f"sensor_{index:02d}"

def date_string(date_str: str):
    '''
    Validation function for use with `argparse`.

    Checks if the passed date string is valid, then returns that same date
    string. Invalid strings will raise a `ValueError`.
    '''

    # Raises a ValueError if the string is invalid.
    datetime.fromisoformat(date_str)
    # Return the same strin that was passed in since no
    # processing is required.
    return date_str

def date_string_lt(date_string_1: str, date_string_2: str):
    '''
    Evaluates whether the first date string represents an earlier point in time
    than the second.
    '''

    # Convert date strings to `datetime` objects and
    # perform comparison.
    return datetime.fromisoformat(date_string_1)\
        < datetime.fromisoformat(date_string_2)

def date_string_gt(date_string_1: str, date_string_2: str):
    '''
    Evaluates whether the first date string represents a later point in time
    than the second.
    '''

    # Convert date strings to `datetime` objects and
    # perform comparison.
    return datetime.fromisoformat(date_string_1)\
        > datetime.fromisoformat(date_string_2)

def validate_analysis_inputs(
        time_start: str,
        time_end: str,
        sensor_start: int,
        sensor_end: int,
    ):
    '''
    Perform validation on the inputs passed to the amalysis functions.

    Only value validation is performed since type validation is handled by
    `argparse` beforehand.
    '''

    # Ensure that the start and end times are within the
    # predefined limits. Also check that the start time is
    # not greater than the end time, as that would not make
    # sense.
    if date_string_lt(time_start, TIME_MIN):
        raise ValueError(f'Start time must be "{TIME_MIN}" or later.')
    if date_string_gt(time_end, TIME_MAX):
        raise ValueError(f'End time must be "{TIME_MAX}" or earlier.')
    if date_string_gt(time_start, time_end):
        raise ValueError('Start time cannot be after end time.')

    # Perform similar vaildation on the sensor indices,
    # ensuring that the start and end indices are within
    # the predefined limits and that the start index is not
    # greater than the end index, since that would, again,
    # not make sense.
    if sensor_start < SENSOR_INDEX_MIN:
        raise ValueError(
            'Sensor start index must be greater than or equal to'
            f' {SENSOR_INDEX_MIN}.'
        )
    if sensor_start < SENSOR_INDEX_MIN:
        raise ValueError(
            'Sensor end index must be less than or equal to'
            f' {SENSOR_INDEX_MAX}.'
        )
    if sensor_start > sensor_end:
        raise ValueError(
            'Sensor start index cannot be greater than sensor end index.'
        )

def subset_df(
        df: DataFrame,
        time_start: str = TIME_MIN,
        time_end: str = TIME_MAX,
        sensor_start: int = SENSOR_INDEX_MIN,
        sensor_end: int = SENSOR_INDEX_MAX,
        ):
    '''
    Select a subset of rows and columns in
    the DataFrame provided, based on a time range
    and a sensor range.
    '''

    # Change indexing column from default (numeric index
    # from CSV file) to 'timestamp' column as we want to
    # index with time. (Solution found on StackOverflow).
    df.reset_index(inplace=True)
    df.set_index('timestamp', inplace=True)

    # Check whether or not the DataFrame is to be used in
    # its entirety, or if a subset is to be selected.
    validate_analysis_inputs(
        time_start,
        time_end,
        sensor_start,
        sensor_end
    )

    # Select the appropriate rows and columns from the
    # DataFrame for processing.
    cells = df.loc[
        time_start:time_end,
        sensor_name(sensor_start):sensor_name(sensor_end)
    ]

    # Convert DataFrame to a list of lists, which is
    # picklable. The data can be parsed back into a Series
    # or DataFrame later when needed. Note that the data is
    # split into column vectors and not row vectors.
    columns = [df[colname].to_numpy() for colname in cells.columns]
    return columns

def get_executor_class(method: str) -> type[ThreadPoolExecutor | ProcessPoolExecutor] | None:
    '''
    Get the executor class based on the passed execution method. If `'sync'` is
    passed, return `None` meaning that the operation should be performed
    synchronously.
    '''

    # Use a match statement since it is cleaner to write it
    # in this way.
    match method:
        case 'thread':
            # If multithreading was requested, use a
            # ThreadPoolExecutor.
            executor_class = ThreadPoolExecutor
        case 'process':
            # If multiprocessing was requested, use a
            # ProcessPoolExecutor.
            executor_class = ProcessPoolExecutor
        case 'sync':
            # If synchronous execution was requested,
            # return None. This will tell the caller to run
            # the tasks synchronously.
            executor_class = None
        case _:
            # If any other value was passed, raise a
            # ValueError
            raise ValueError(
                '`method` argument must be either `thread`, `process` or'
                ' `sync`.'
            )

    return executor_class

def get_summaries_per_df():
    '''
    Estimate how many DataFrame columns should fit within the terminal window
    and, thus, how many column summaries each result-bearing DataFrame should
    contain, at most.
    '''

    # Get the width of the terminal.
    width, _ = get_terminal_size()

    # A Series or DataFrame description returns a Series.
    # The longest row naem in this resultant Series object
    # is "count", which is 5 characters long. The column
    # width is determined by the COLUMN_WIDTH variable.

    # Thus, to find how many columns can fit inside the
    # terminal window, one must subtract 5 from the
    # terminal width, and divide the result by the column
    # width. Integer division must be used since we want to
    # truncate any decimal points and round down every
    # time.
    return (width - 5) // COLUMN_WIDTH
