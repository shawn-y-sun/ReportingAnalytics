from Reporting import load_data, Write, template_auto_bk, brul3
import time
import datetime

if __name__ == "__main__":
    start = time.time()
    ################################################

    file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_reporting.csv'
    df = load_data(file_name)
    print('*************************')
    print('Generating Report ...')
    b = Write(template_auto_bk, df, brul3)
    b.time_frame(start=20181101)
    # b.write()
    c = b.copy()
    c.df = b.df_incr_ttl
    c.write()

    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')