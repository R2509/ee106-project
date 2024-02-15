'''
Definition of MultiCoreManager class.
'''

from multiprocessing import JoinableQueue, Process, cpu_count
from typing import Any, Callable


class MultiCoreManager:
    '''
    Manages running processes across multiple cores.
    '''
    def __init__(self):
        # Declare instance variables
        self.core_count: int
        self.cores_in_use: int
        self.process_queue: list[Callable[..., Any]]
        self.queue: JoinableQueue

        # Initialise data
        self._load()

    def _load(self):
        self.core_count = cpu_count()
        self.cores_in_use = 0
        self.process_queue = []
        self.queue = JoinableQueue()

    def add_to_queue(self, *processes: Callable[..., Any]):
        '''
        Add a process to the queue. Must be run before.
        '''
        # Add passed processes to the queue.
        self.process_queue.extend(processes)

    def _wrap_func(self, func: Callable[..., Any]) -> Callable[[JoinableQueue], None]:
        # Wrap the function to make results available to main code
        def proc(queue: JoinableQueue):
            # One more core is being used to run process
            self.cores_in_use += 1

            # Run function
            func_result = func()
            queue.put(func_result)

            # Core is now freed
            self.cores_in_use -= 1
        return proc

    def _create_process(self, proc_index: int):
        func = self.process_queue[proc_index]
        proc = self._wrap_func(func)
        process = Process(
            target = proc,
            args = (self.queue, ),
        )
        return process
    def _start_process(self, process_index: int):
        self.process_queue[process_index]
    def _wait_until_done(self):
        self.queue.join()
    def start_processes(self):
        '''
        Start running all the processes.
        '''
        proc_queue_index = 0
        while self.cores_in_use < self.core_count \
        and proc_queue_index < len(self.process_queue):
            process = self._create_process(proc_queue_index)
            process.start()
            proc_queue_index += 1
