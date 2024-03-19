import sys
from time import perf_counter
from typing import Any, Callable
from util import CLEAR_SCREEN


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

                #TODO: DIUCMENT
                start_time = perf_counter()
                result = task(*args, **kwargs)
                duration = perf_counter() - start_time

                sys.stdout.write(f'{task_completed_message} ({duration}).\n')
                sys.stdout.flush()

                return result
            return inner
        return wrapper

    def clear_terminal(self):
        '''
        Clear all text on the terminal window and reset the cursor position to
        the top left of the terminal window.
        '''
        self.log(CLEAR_SCREEN)

logger = Logger()
