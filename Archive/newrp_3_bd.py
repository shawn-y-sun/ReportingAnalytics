from Reporting import load_data, Write, template_new_bd_strat_v3, st_brul3_test
import time
import datetime

if __name__ == "__main__":
    start = time.time()
    ################################################

    file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_reporting.csv'
    df = load_data(file_name)
    print('*************************')
    print('Generating Report ...')
    b = Write(template_new_bd_strat_v3, df, st_brul3_test)
    b.time_frame(frame=(20190801, 20200331))
    b.write()

    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')