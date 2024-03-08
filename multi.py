'''
Definition of MultiCoreManager class.
'''

from concurrent.futures import ProcessPoolExecutor

from csv_man import CSVManager

def something(x: int):
    return x ** 2

def generate_columns(csv_manager: CSVManager, start: int, end: int):
    return csv_manager.select_column_range(start, end)


if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        arr = executor.map(something, )
    print([x for x in arr])
