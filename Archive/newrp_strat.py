from Reporting import load_data, Write, template_new_strat_fy, template_new_strat_cy
import time
import datetime

if __name__ == "__main__":
    start = time.time()
    ################################################
    df = load_data()
    print('*************************')
    print('Generating Fiscal Yearly Report ...')
    b = Write(template_new_strat_fy, df)
    b.write()

    # print('*************************')
    # print('Generating Calendar Yearly Report ...')
    # c = Write(template_new_strat_cy, df)
    # c.write()
    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')