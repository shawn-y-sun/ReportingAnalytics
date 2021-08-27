from Reporting import load_data, Write, template_new_v4, st_brul3_test
import time
import datetime

data_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_reporting.csv'
save_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report'

if __name__ == "__main__":
    start = time.time()

    ################################################

    df = load_data(data_path)
    rp = Write(template_new_v4, df, st_brul3_test)
    rp.dir = save_path
    rp.time_frame(start=20181101)
    rp.write()

    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')