from Reporting import load_data, Print, \
    filter_tdsr_sim, filter_bad_tdsr, filter_bad_no_tdsr, \
        st_tdsr, Metrics, filter_tdsr_sim_notblocked, Print

file_path_1 = r'C:\Users\sunsh\Documents\TDSR A Decline\TDSRA_over65_makingitthrough_noTDSRrule.xlsx'
file_path = r'C:\Users\sunsh\Documents\Data\cibc_output_file_jun2018_to_sep2020.csv'
if __name__ == "__main__":
    #print(filter_bad_tdsr.query)

    df_dec = load_data(file_path_1)
    df = load_data(file_path)

    # print('Generating Report  ...')

    # m_dec = Metrics(df, strategy=st_tdsr)
    # m_dec.time_frame(frame=(20180601, 20190830))
    # df_vlt = m_dec.df_vlt_ttl

    # m_vlt = Metrics(df_vlt)

    # df_d = m_vlt.dfd
    # m_d = Metrics(df_d)
    
    # df_d_bk = m_vlt.dfd_bk
    # m_d_bk = Metrics(df_d_bk)
    # ## Initial Analysis
    # print(f'''
    # Vol(booked): {m_vlt.tl_bk}
    # Amt: {m_vlt.tl_bk_ln}

    # Bad vol: {m_vlt.tl_bk_bd}
    # Bad Balance: {m_vlt.tl_bk_bd_bal}
    # Bad Rate: {m_vlt.tl_bk_bd_r}

    # Declines: {m_vlt.tl_d}
    # Decline Amt: {m_d.tl_ttd_ln}

    # Manual Declines: {m_vlt.tl_md}
    # Auto Declines: {m_vlt.tl_ad}

    # Decline but booked elsewhere: {m_d_bk.tl_ttd}
    # Decline and booked amt: {m_d_bk.tl_ttd_ln}

    # ''')

    # m_dec = Metrics(df, strategy=st_tdsr)
    # m_dec.time_frame(frame=(20200501, 20200831))
    # df_vlt = m_dec.df_vlt_ttl

    m_vlt = Metrics(df_dec)

    df_m = m_vlt.dfm
    df_md = m_vlt.dfmd

    p_m = Print(df_m)
    p_md = Print(df_md)

    p_m.show('cs_ttd')
    p_md.show('cs_ttd')


    
    ## Benefits
    a = Print(df, strategy=st_tdsr, filter=filter_tdsr_sim_notblocked)
    a.time_frame(frame=(20200501, 20200831))
    ab_65 = a.tl_vlt
    print('Total Pop of TDSR A >65: ', ab_65)

    a.apply_filter()

    print('Flag Analysis ..')
    print('\nNot Blocked: ', a.tl_ttd)
    print('Blocked: ', ab_65 - a.tl_ttd)
    print('\nManually Approved: ', a.tl_m)
    print('Manually Declined: ', a.tl_md)


    print('\nTotal Approved Vol: ', a.tl_ttd_ln)
    ma_m = Metrics(a.dfm)
    print('Manually Approved Vol: ', ma_m.tl_ttd_ln)
    ma_md = Metrics(a.dfmd)
    print('Manually Declined Vol: ', ma_md.tl_ttd_ln)


    ## Flag Analysis
    a = Print(df, strategy=st_tdsr, filter=filter_tdsr_sim)
    a.time_frame(frame=(20200501, 20200831))
    a.apply_filter()
    print('\nttd shape: ', a.df.shape)
    flags = ["DIVESTITURE_FLAG", "UW47_FLAG","COMMERCIALVEHICL_FLAG","UW43_FLAG","UW62_FLAG","UW40_FLAG"
            ,"UW79_FLAG","UW74_FLAG","UW68_FLAG","LIGHTDUTY_FLAG","UW45_FLAG","UW63_FLAG","CIBCERROR_FLAG"
            ,"UW8_FLAG","UW26_FLAG","UW33_FLAG","UW72_FLAG","UW9_FLAG","UW2_FLAG","UW16_FLAG"
            ,"BCN_AUTO_DEC_FLAG","UW190_FLAG","UW27_FLAG","HIGHPTI_FLAG","UW28_FLAG","UW29_FLAG","UW85_FLAG"
            ,"UW86_FLAG","UW80_FLAG","UW83_FLAG","UW82_FLAG","FTIERNOTNEWCOMER_FLAG","AGEINCOME_FLAG",
            "UW50_FLAG","CRISTATCODEERR_FLAG","LOWTOTALINCOME_FLAG","CB7_FLAG","AUTOAPPROVETIERC_FLAG",
            "UW71_FLAG","UW6_FLAG","UW21_FLAG",
            ]
    
    ttd_flag = a.df[flags]
    flag_dist_new=ttd_flag.sum(axis=0) 
    flag_dist_new.sort_values(ascending=False, inplace=True)
    print('\nTTD Flag Analysis: ', flag_dist_new.head(45))

    print('Declined Flag Analysis ..')
    print('Declined shape: ', a.dfd.shape)
    d_flags = a.dfd[flags]
    flag_dist_new=d_flags.sum(axis=0) 
    flag_dist_new.sort_values(ascending=False, inplace=True)
    print('\nDeclined Flag Analysis: ', flag_dist_new.head(45))

    print('Manual Declined Flag Analysis ..')
    print('Manual Declined shape: ', a.dfmd.shape)
    md_flags = a.dfmd[flags]
    flag_dist_new=md_flags.sum(axis=0) 
    flag_dist_new.sort_values(ascending=False, inplace=True)
    print('\nManual Declined Flag Analysis: ', flag_dist_new.head(45))


    ### Bad Rates
    ## With UW58
    b = Print(df, filter=filter_bad_tdsr)
    b.time_frame(end=20190831)
    b.apply_filter()
    print('\nBooked Tier A Blocked shape (booked): ', b.dfbk.shape)
    print('\nBooked Tier A Blocked shape (booked and bad): ', b.dfbk_bd.shape)
    print('All Booked: ', b.tl_bk_bd_r)

    ## Without UW58
    c = Print(df, filter=filter_bad_no_tdsr)
    c.time_frame(end=20190831)
    c.apply_filter()
    print('\nBooked Tier A Blocked shape (no UW58): ', c.dfbk.shape)
    print('\nBooked Tier A Blocked shape (booked and bad): ', c.dfbk_bd.shape)
    print('All Booked: ', c.tl_bk_bd_r)




