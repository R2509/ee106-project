'''
PARRALLEL PROCESSING ENGINE
'''

import multiprocessing as mp
from pathlib import Path
import pandas as pd
import tkinter as tk
import numpy as np
from time import sleep


dir_path = Path(__file__).parent.resolve()

## each function of pandas get an function to do a multithread processing thingy

# ClassName
# variable_or_function_name



def open_csv():
    #    global ReadFile
    ReadFile = pd.read_csv(dir_path / "sensor_timeseries.csv")

proc_1 = mp.Process(target=open_csv)









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




def create_process_task():
    if True: pass # REPLACE THIS WITH WHATEVER
