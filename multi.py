'''
Definition of MultiCoreManager class.
'''

from multiprocessing import JoinableQueue, Process, cpu_count
from typing import Any, Callable
from time import sleep


class MultiCoreManager:
    '''
    Manages running processes across multiple cores.
    '''
    def __init__(self):
        # Declare instance variables. It has been layed out in this
        # way to increase readability. Initial values are assigned in
        # `self._load()`

        # The number of cores that the device has.
        self.core_count: int

        # The number of cores currently in use. This is used when
        # queueing processes.
        self.cores_in_use: int

        # The number of processes that have been completed
        self.process_index: int

        # Contains wrapped processes. Raw functions are not needed.
        self.process_queue: list[Callable[..., Any]]

        # An object which allows communication between
        # processes and the main thread.
        self.queue: JoinableQueue

        # Initialise data
        self._load()

    def _load(self):
        self.core_count = cpu_count()
        self.cores_in_use = 0
        self.process_index = 0
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

            # Tell the queue that we are finished
            queue.task_done()

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
    def _start_next_process(self):
        process = self._create_process(self.process_index)
        process.start()
        self.process_index += 1

    def _wait_until_done(self):
        self.queue.join()
    def start_processes(self):
        '''
        Start running all the processes.
        '''
        # Reset counter
        self.process_index = 0

        # Use polling to check when cores are available.
        # Loop while there are still processes to be added.
        while self.process_index < len(self.process_queue):
            # If we have any cores available
            # (that aren't already running tasks)
            if self.cores_in_use < self.core_count:
                # Start up the next process.
                self._start_next_process()
            else:
                # Poll every 0.1 seconds.
                sleep(0.1)

        # Wait until all processes have finished executing.
        self._wait_until_done()

        # debug
        data = self.queue.get()
        print(data)

def add_two(a: int, b: int):
    '''
    Test function that adds two numbers.
    '''
    return a + b

if __name__ == '__main__':
    mcm = MultiCoreManager()
    mcm.add_to_queue(add_two)
    mcm.start_processes()

# AttributeError: Can't pickle local object 'MultiCoreManager._wrap_func.<locals>.proc'
