'''k
'''
import pandas as pd;

from pathlib import Path

dir_path = Path(__file__).parent.resolve()

pd.read_csv(dir_path / 'sensor_timeseries.csv')

