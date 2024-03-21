import sys
from time import perf_counter
from typing import Any, Callable
from util import CLEAR_SCREEN, TEXT_CYAN, TEXT_RED, TEXT_RESET


'''
Logging utilities. Used throughout code instead of builtins so that
logging can be controlled as needed, and to make the rest of the code
cleaner.
'''

def _log(message: str, flush: bool):
    sys.stdout.write(message)
    if flush:
        # Ensure that the output gets printed immediately.
        sys.stdout.flush()

def log(message: str, flush: bool = True) -> None:
    '''
    Basic alternative to `print()`.
    '''
    _log(message, flush)

def info(message: str, flush: bool = True):
    '''
    Similar to `log()`, but prints an informational message (in blue text).
    '''
    _log(f'{TEXT_CYAN}{message}{TEXT_RESET}', flush)

def error(message: str, flush: bool = True):
    '''
    Similar to `log()`, but prints an error message (in red text).
    '''
    _log(f'{TEXT_RED}{message}{TEXT_RESET}', flush)

def log_task(
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

            #TODO: DIUCMENT
            start_time = perf_counter()
            result = task(*args, **kwargs)
            duration = perf_counter() - start_time

            sys.stdout.write(f'{task_completed_message} ({duration}).\n')
            sys.stdout.flush()

            return result
        return inner
    return wrapper

def clear_terminal():
    '''
    Clear all text on the terminal window and reset the cursor position to
    the top left of the terminal window.
    '''
    _log(CLEAR_SCREEN)
