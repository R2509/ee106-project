'''
AUTHOR(S):
    james Robertson
    rison padayachy

THIS A TEST UPLOAD TO TEST THAT I CAN COMMIT NEW FILES/CODE








 /home/james/anaconda3/envs/python312

'''
import pandas as pd;

from pathlib import Path

dir_path = Path(__file__).parent.resolve()

pd.read_csv(dir_path / 'sensor_timeseries.csv')

