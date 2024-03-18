# take in pandas dataframe and split into 4 tasks

# in the csv only 52 sensors - 8 
from time import pthread_getcpuclockid
import pandas as pd 




## below not reqd in this file!
full_data_frame = pd.read_csv("sensor_timeseries.csv")
print(full_data_frame.nunique())
'''
data_frame_only_sensor_data = full_data_frame.iloc[:, 2:-1]
#print(data_frame_only_sensor_data)
#print(full_data_frame)
'''
def range_selector(start_time, end_time, accept_error):
    pass
def time_selector(time):
    pass
'''
#print(len(data_frame_only_sensor_data.columns))
def data_splitter(dfin):
    num_cols = len(dfin.columns)
    # create 8 tasks
    num_cols_first_proc = (num_cols//8) # gets how many columns should be handled for the first 7 of 8 processes
    # optimise efficiency with relativley even work distribution
    num_cols_last_proc = num_cols - (num_cols_first_proc * 7) # gets how many columns should be handled for the last process

    print(num_cols_last_proc)
    #
    df1 = dfin.iloc[:, 0:num_cols_first_proc]
    df2 = dfin.iloc[:, num_cols_first_proc:num_cols_first_proc*2]
    df3 = dfin.iloc[:, num_cols_first_proc*2:num_cols_first_proc*3]
    df4 = dfin.iloc[:, num_cols_first_proc*3:num_cols_first_proc*4]
    df5 = dfin.iloc[:, num_cols_first_proc*4:num_cols_first_proc*5]
    df6 = dfin.iloc[:, num_cols_first_proc*5:num_cols_first_proc*6]
    df7 = dfin.iloc[:, num_cols_first_proc*6:num_cols_first_proc*7]
    df8 = dfin.iloc[:, num_cols_first_proc*7:num_cols_first_proc*8]
    df9 = dfin.iloc[:, num_cols_first_proc*8:num_cols] # creates a small task for remaining columns


    print(df8)
    return df1, df2, df3, df4, df5, df5, df6, df7, df8, df9
data_splitter(data_frame_only_sensor_data)
'''