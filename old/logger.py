import sys
from dataclasses import dataclass
from typing import Callable


class Logger:
    def __init__(
            self,
            task_running_str: str = '... ',
            task_done_str = 'Complete',
        ):
        self.task_running_str = task_running_str
        self.task_done_str = task_done_str
    def log(self, message: str):
        sys.stdout.write(message)

    def log_task(self, task: Callable, message: str) -> Callable:
        def wrapper(*args, **kwargs):
            sys.stdout.write(f'{message}{self.task_running_str}')
            sys.stdout.flush()

            result = task(*args, **kwargs)

            sys.stdout.write(f'{self.task_done_str}\n')
            sys.stdout.flush()

            return result
        return wrapper

logger = Logger()
