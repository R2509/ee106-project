# removes error lined from the dataframe

# where final col in df is not "NORMAL"

# use multiprocessing

import pandas as pd
import multiprocessing as mp



def clean_dataframe(data_frame_in):
    for loop in range(len(data_frame_in)):
        # if col last != normal then remove it 