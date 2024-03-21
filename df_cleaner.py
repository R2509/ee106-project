import logger

# removes error lined from the dataframe

# where final col in df is not "NORMAL"



import pandas
# Import relevant 

dfrm = pandas.read_csv("sensor_timeseries.csv")
err_rows = []




def clean_dataframe(data_frame_in: pandas.DataFrame):
 
    for row_index in range(0, len(data_frame_in)):
        # if col last != normal then remove it

        if data_frame_in.at[row_index, 'machine_status'] != "NORMAL":
            # if the dataframe has ann error or recovering state at this particilar row do below items
            err_rows.append(row_index)
            # Append rows with errors to list of eror rows
            
    data_frame_out = data_frame_in.drop(err_rows)
    logger.log(f"there was {str(len(err_rows))} rows containing errors\n    all removed successfully")
   # print(data_frame_out)

    #print(err_rows)
    return data_frame_out


_ = (clean_dataframe(dfrm))



#\x1b[2J\x1b[A
