'''
Contains general utilities used throughout the program.
'''

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
import sys
from typing import Any, Callable
from pandas import DataFrame

TIME_MIN = datetime(2018, 4, 1)
TIME_MAX = datetime(2018, 8, 31)

SENSOR_INDEX_MIN = 0
SENSOR_INDEX_MAX = 51


def sensor_name(index: int):
    '''Generates a sensor name from an index.'''
    return f"sensor_{index:02d}"

def date_string(date_str: str):
    '''
    Validation function for use with `argparse`.

    Checks if the passed date string is valid, then returns that same date
    string. Invalid strings will raise a `ValueError`.
    '''

    # Raises a ValueError if the string is invalid.
    datetime.fromisoformat(date_str)

    return date_str


class Logger:
    '''
    Logging utilities. Used throughout code instead of builtins so that
    logging can be controlled as needed, and to make the rest of the code
    cleaner.
    '''
    def __init__(self) -> None:
        return

    def log(self, message: str, flush=True) -> None:
        '''
        Basic alternative to `print()`.
        '''
        sys.stdout.write(message)
        if flush:
            # Ensure that the output gets printed immediately.
            sys.stdout.flush()

    def log_task(
            self,
            message: str,
            task_completed_message: str = 'Complete',
        ):
        '''
        Wraps a function so that a message is printed before the function is
        run, and a completion message is printed once the function has exited.

        Written decorator-style, however it can be used directly.

        Usage example:
        ```python
        def my_task(text: str):
            return f'you passed "{text}"!'
        
        logger = Logger()
        task_result = logger.log_task('Starting task... ')(my_task)('Hello')
        logger.log(task_result)
        
        >>> Starting task... Complete
        >>> You passed "Hello"!
        ```
        '''
        def wrapper(task: Callable):
            def inner(*args: Any, **kwargs: Any): # Return type same as task
                self.log(message)

                result = task(*args, **kwargs)

                sys.stdout.write(f'{task_completed_message}\n')
                sys.stdout.flush()

                return result
            return inner
        return wrapper


def subset_df(
        df: DataFrame,
        time_start: datetime = TIME_MIN,
        time_end: datetime = TIME_MAX,
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
            sensor_name(sensor_start):sensor_name(sensor_end)
        ]

    # Convert DataFrame to a list of lists, whic is picklable. The data can be
    # parsed back into a Series or DataFrame later when needed.
    # Note that the data is split column-wise.
    columns = [df[colname].to_numpy() for colname in cells.columns]
    return columns

def get_executor_class(method: str) -> type[ThreadPoolExecutor | ProcessPoolExecutor] | None:
    match method:
        case 'thread':
            executor_class = ThreadPoolExecutor
        case 'process':
            executor_class = ProcessPoolExecutor
        case 'sync':
            executor_class = None
        case _:
            raise ValueError(
                '`method` argument must be'
                'either `thread` or `process`.'
            )

    return executor_class


logger = Logger()
