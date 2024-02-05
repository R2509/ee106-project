'''
PARRALELL PROCESSIN' ENGINE
what the actual fuck is this meant to do 


'''

from time import sleep 
import multiprocessing as mp
from pathlib import Path
import pandas as pd
import tkinter as tk
import numpy as numpy





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





## addition of code from 2feb24(friday lab)

'''
PARRALLEL PROCESSING ENGINE
'''
'''
import multiprocessing as mp
from pathlib import Path
import pandas as pd
import tkinter as tk
import numpy as numpy





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
    if 

'''