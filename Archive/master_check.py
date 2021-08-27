from Reporting import load_data, Print, brul3, filter_sys_aap_brul3
import time
import datetime

if __name__ == "__main__":
    start = time.time()
    ################################################

    file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\z4\new z4\master_newz4.csv'
    df = load_data(file_name)

#####

    pt = Print(df, brul3, filter_sys_aap_brul3)
    pt_incr = pt.copy()
    pt_incr.df = pt.df_incr_ttl
    pt_noincr = pt.copy()
    pt_noincr.df = pt.df_no_incr_aap_ttl

    print('\n2021')
    pt_21 = pt.copy()
    pt_21_noincr = pt_noincr.copy()
    pt_21_noincr.time_frame(start=20210601, end=20210630)
    print(pt_noincr.tl_aap_r)
    print(pt_noincr.tl_m_r)
    print(pt_noincr.tr_aap_r)
    print(pt_noincr.tr_m_r)
    print(pt_noincr.tl_ap_r)


    print('\n2020')
    pt_20 = pt.copy()
    pt_20.time_frame(start=20201001, end=20201031)
    print(pt_20.tl_aap_r)
    print(pt_20.tl_m_r)
    print(pt_20.tr_aap_r)
    print(pt_20.tr_m_r)
    print(pt_20.tl_ap_r)

    ###############################################
    end = time.time()
    time_secs = end - start

    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'Runtime of the program is {time_str}')