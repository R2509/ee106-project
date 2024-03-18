

# removes error lined from the dataframe

# where final col in df is not "NORMAL"

# use multiprocessing perhaps

from tarfile import data_filter
import pandas
import multiprocessing as mp

dfrm = pandas.read_csv("sensor_timeseries.csv")
err_rows = []

dfrm.drop([1])
print(dfrm)




def clean_dataframe(data_frame_in):
    err_prev = False
    for rows in range(0, len(data_frame_in)):
        # if col last != normal then remove it

        if data_frame_in.iat[rows, 54] != "NORMAL":
            
            


        err_rows.append(rows)
           # print(" ERROR FOUND AT LINE", rows)
    #print(err_rows)
    data_frame_in = data_frame_in.drop(err_rows)
    
    
    for rows in range(0, len(data_frame_in)):
        # if col last != normal then remove it

        if data_frame_in.iat[rows, 54] != "NORMAL":
            
            print(" ERROR FOUND AT LINE", rows, "row not deleted")
    
        #print(data_frame_in.iat[rows, 54],rows)


clean_dataframe(dfrm)

#\x1b[2J\x1b[A