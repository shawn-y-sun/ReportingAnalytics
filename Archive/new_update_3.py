from Reporting import load_data, Write, template_new_fy_strat_v3
import time
import datetime

if __name__ == "__main__":
    start = time.time()

    ################################################

    # Load New Data
    df = load_data()

    print('Updating Report ...')

    # ## Monthly update
    # a = Write(template_new_fy_mth_v2, df)
    # a.time_frame(start=20210701, end=20210730)
    # a.write()

    ## Strat Update
    a = Write(template_new_fy_strat_v3, df)
    a.time_frame(start=20210512)
    a.write()

    print('!Report Updated')
    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'[Runtime of the program is {time_str}]')