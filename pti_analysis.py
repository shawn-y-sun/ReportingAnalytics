from Reporting import load_data, Metrics, st_pti_b, st_pti_23, filter_lightduty

file_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\New Dataset - May12July13_bookings.xlsx'

if __name__ == '__main__':
    df = load_data(file_path)
    met = Metrics(df, st_pti_23, filter_lightduty)

    ## May 12 - May 31
    print('\nMay 12 - May 31')
    met_may = met.copy()
    met_may.time_frame(frame=(20210512, 20210531))
    print(f'TTD: {met_may.tl_ttd}')
    print(f'TTD(ABC): {met_may.tl_ttdt}')
    print(f'Auto Approved: {met_may.tl_aap}')
    print(f'Auto Approved Rate: {met_may.tl_aap_r}')
    print(f'Auto Approved (ABC): {met_may.tl_aapt}')
    print(f'Auto Approved Rate (ABC): {met_may.tl_aapt_r}')


    print('\nTier TTD')
    print(met_may.tr_ttd)
    print('Tier Auto Approved')
    print(met_may.tr_aap)
    print('Tier Booked')
    print(met_may.tr_bk)

    met_may_strat = met_may.copy()
    met_may_strat.df = met_may_strat.df_incr_ttl
    print("\nPTI (15-23)")
    print('Tier TTD:')
    print(met_may_strat.tr_ttd)
    print('Tier Booked:')
    print(met_may_strat.tr_bk)

    met_may_pti20 = met_may.copy()
    met_may_pti20.strategy = st_pti_b
    met_may_pti20.df = met_may_pti20.df_incr_ttl
    print("\nPTI (15-20)")
    print('Tier TTD:')
    print(met_may_pti20.tr_ttd)
    print('Tier Auto Approved:')
    print(met_may_pti20.tr_aap)
    print('Tier Booked:')
    print(met_may_pti20.tr_bk)

    met_may_vlt = met_may.copy()
    met_may_vlt.df = met_may_vlt.df_vlt_ttl
    print("\nPTI (>23)")
    print('Tier TTD:')
    print(met_may_vlt.tr_ttd)
    print('Tier Booked:')
    print(met_may_vlt.tr_bk)


    print("\nPTI (15-20) Manual Approved")
    met_may_pti_b = met_may.copy()
    met_may_pti_b.strategy = st_pti_b
    print(met_may_pti_b.tl_ttd)
    print(met_may_pti_b.tl_aap)
    print(met_may_pti_b.tl_aap_r)
    met_may_pti_b.df = met_may_pti_b.df_incr_ttl
    print(met_may_pti_b.tr_m)


    print('\nLightDuty Booking')
    met_may_light = met_may.copy()
    met_may_light.apply_filter()
    print(met_may_light.tr_ttd)
    print(met_may_light.tr_aap)
    print(met_may_light.tr_bk)


    ## June 4 - June 21
    print('\nJune 4 - June 21')
    met_june = met.copy()
    met_june.time_frame(frame=(20210604, 20210621))
    print(f'TTD: {met_june.tl_ttd}')
    print(f'TTD(ABC): {met_june.tl_ttdt}')
    print(f'Auto Approved: {met_june.tl_aap}')
    print(f'Auto Approved Rate: {met_june.tl_aap_r}')
    print(f'Auto Approved (ABC): {met_june.tl_aapt}')
    print(f'Auto Approved Rate (ABC): {met_june.tl_aapt_r}')


    print('Tier TTD')
    print(met_june.tr_ttd)
    print('Tier Auto Approved')
    print(met_june.tr_aap)
    print('Tier Booked')
    print(met_june.tr_bk)

    met_june_strat = met_june.copy()
    met_june_strat.df = met_june_strat.df_incr_ttl
    print("\nPTI (15-23)")
    print('Tier TTD:')
    print(met_june_strat.tr_ttd)
    print('Tier Booked:')
    print(met_june_strat.tr_bk)

    met_june_pti20 = met_june.copy()
    met_june_pti20.strategy = st_pti_b
    met_june_pti20.df = met_june_pti20.df_incr_ttl
    print("\nPTI (15-20)")
    print('Tier TTD:')
    print(met_june_pti20.tr_ttd)
    print('Tier Auto Approved:')
    print(met_june_pti20.tr_aap)
    print('Tier Booked:')
    print(met_june_pti20.tr_bk)

    met_june_vlt = met_june.copy()
    met_june_vlt.df = met_june_vlt.df_vlt_ttl
    print("\nPTI (>23)")
    print('Tier TTD:')
    print(met_june_vlt.tr_ttd)
    print('Tier Booked:')
    print(met_june_vlt.tr_bk)

    print('\nLightDuty Booking')
    met_june_light = met_june.copy()
    met_june_light.apply_filter()
    print(met_june_light.tr_ttd)
    print(met_june_light.tr_aap)
    print(met_june_light.tr_bk)


    

    ## Strat
    print('Strat June4 - 30')
    met_june30_strat = met.copy()
    met_june30_strat.time_frame(frame=(20210604, 20210630))
    met_june30_strat.strategy = st_pti_b
    met_june30_strat.df = met_june30_strat.df_incr_ttl

    print(f'TTD: {met_june30_strat.tl_ttd}')
    print(f'Auto Approved: {met_june30_strat.tl_aap}')
    print(f'Auto Approved Rate: {met_june30_strat.tl_aap_r}')
    print(f'Auto Approved (ABC): {met_june30_strat.tl_aapt}')
    print(f'Auto Approved Rate (ABC): {met_june30_strat.tl_aapt_r}')

    print("PTI (15-20)")
    print("Total Incr")
    print(met_june30_strat.tl_incr)
    print("Tier Incr")
    print(met_june30_strat.tr_incr)
    print("Total Incr aap")
    print(met_june30_strat.tl_incr_aap)
    print("Tier Incr aap")
    print(met_june30_strat.tr_incr_aap)



