from argparse import Namespace
from datetime import datetime
from pathlib import Path

from proc import summarise_file, logger
from util import date_string


this_dir = dirpath = Path(__file__).resolve().parent

def generate_summary(ns: Namespace):
    data, time_taken = summarise_file(
        this_dir / ns.file_path,
        method = ns.method,
        time_range = (ns.time_start, ns.time_end),
        sensor_range = (ns.sensor_start, ns.sensor_end),
    )
    logger.log(f'{data}\n\r\n\rProcessing took {time_taken:.3f} seconds.')

commands = [
    (
        'summary',
        generate_summary,
        'Generate a summary of the data file specified.',
        [
            (
                ['-f', '--file-path'],
                {
                    'action': 'store',
                    'help': 'The relative path of the file to analyse. Defaults'
                                ' to the sensor time-series file.',
                    'default': './sensor_timeseries.csv',
                    'type': Path,
                },
            ),
            (
                ['-ss', '--sensor-start'],
                {
                    'action': 'store',
                    'help': 'The sensor number to start at. Defaults to 0.',
                    'default': '0',
                    'type': int,
                },
            ),
            (
                ['-se', '--sensor-end'],
                {
                    'action': 'store',
                    'help': 'The sensor number to stop at. Defaults to 51.',
                    'default': '51',
                    'type': int,
                },
            ),
            (
                ['-ts', '--time-start'],
                {
                    'action': 'store',
                    'help': 'The time to start at. Defaults to'
                                   ' "2018-04-01 00:00:00".',
                    'default': '2018-04-01 00:00:00',
                    'type': date_string,
                },
            ),
            (
                ['-te', '--time-end'],
                {
                    'action': 'store',
                    'help': 'The time to stop at. Defaults to'
                                   ' "2018-08-31 23:59:00".',
                    'default': '2018-08-31 23:59:00',
                    'type': date_string,
                },
            ),
            (
                ['-m', '--method'],
                {
                    'action': 'store',
                    'help': 'The method to use when executing the'
                                   ' tasks. Can be either "process" or'
                                   ' "thread". Defaults to "process".',
                    'default': 'process',
                },
            ),
        ],
    ),
]