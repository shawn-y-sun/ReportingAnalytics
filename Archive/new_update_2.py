from Reporting import load_data, Write, template_new_fy_strat_v2, \
    cf_new_v2, add_slicers, template_new_fy_mth_v2
import time
import datetime

if __name__ == "__main__":
    start = time.time()

    ################################################

    # Load New Data
    df = load_data()

    print('Generating Fiscal Yearly Report ...')

    # ## Monthly update
    # a = Write(template_new_fy_mth_v2, df)
    # a.time_frame(start=20210701, end=20210730)
    # a.write()

    ## Strat Update
    a = Write(template_new_fy_strat_v2, df)
    #a.time_frame(end=20210531)
    a.write()

    # Creating Charts
    print('Adding Charts ...')
    cf_new_v2.write(merge=True, hide=True)

    print('Adding Slicers ...')
    add_slicers(cf_new_v2.destination)

    print('!Report Updated')
    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'[Runtime of the program is {time_str}]')