from Reporting import load_data, Write, template_new_profile
import time
import datetime

if __name__ == "__main__":
    start = time.time()
    ################################################

    df = load_data()
    print('*************************')
    print('Generating Fiscal Yearly Report ...')
    b = Write(template_new_profile, df)
    b.time_frame(start=20191101)
    b.write()

    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')