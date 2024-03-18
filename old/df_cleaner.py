# removes error lined from the dataframe

# where final col in df is not "NORMAL"

# use multiprocessing perhaps

import pandas
import multiprocessing as mp

dfrm = pandas.read_csv("sensor_timeseries.csv")

def clean_dataframe(data_frame_in):
    for rows in range(0, len(data_frame_in)):
        # if col last != normal then remove it

        if data_frame_in.iat[rows, 52] != "normal":
            print("\r ERROR FOUND AT LINE", rows)

clean_dataframe(dfrm)
d