from Reporting import Dataset, load_data, Print, brul3, filter_sys_aap_brul3, filters_brul3, filters_brul3_w_uw21
import time
import datetime

data_file = r"Data/cibc_output_file_jun2018_to_sep2020.csv"

if __name__ == "__main__":
    start = time.time()
    ################################################
    df = load_data(data_file)
    pr_ds = Print(df, brul3, filters_brul3_w_uw21)
    pr_ds.time_frame(frame=(20200501, 20200831))
    pr_ds.apply_filter(mode=True)
    pr_ds.filter = filter_sys_aap_brul3
    pr_ds.apply_filter(mode=False)

    pr_ds.show('dc_ttd')
    pr_ds.show('tr_ttd')
    pr_ds.show('csg_ttd')
    pr_ds.show('tr_ttd_ln')
    pr_ds.show('tr_m')
    pr_ds.show('tl_ttd_bbc')
    pr_ds.show('tr_ttd_pti')
    pr_ds.show('tr_ttd_ltv')
    pr_ds.show('tr_ttd_tdsr')
    pr_ds.show('tl_ttd_cbage')
    pr_ds.show('tl_ttd_ot')




    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')