'''
PARRALELL PROCESSIN' ENGINE


'''

from time import sleep 
import multiprocessing as mp
from pathlib import Path
import pandas as pd
import tkinter as tk




dir_path = Path(__file__).parent.resolve()

pd.read_csv(dir_path / 'sensor_timeseries.csv')













'''
def test():
    for loop in range (100):
        sleep(0.1)
        print('hello')
  
def test2():
    for loop in range(100):
        sleep(0.1)
        print("ass")


pr1 = mp.Process(target=test)
pr2 = mp.Process(target=test2)
pr2.start()
pr1.start()
pr2.join()
pr1.join()

print("th")
'''