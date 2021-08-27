from Reporting import load_data, Metrics

file_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\newest z4\master_june_july_2021.csv'

if __name__ == '__main__':
    df = load_data(file_path)
    met = Metrics(df)
    met.time_frame(frame=(20210701,20210731))

    print(f'TTD: {met.tl_ttd}')
    print(f'Total Approved: {met.tl_ap}')
    print(f'Total Declined: {met.tl_d}')
    print(f'Total Booked: {met.tl_bk}')
    print(f'Auto Approved: {met.tl_aap}')
    print(f'Auto Declined: {met.tl_ad}')
    print(f'Manual Approved: {met.tl_m}')
    print(f'Manual Declined: {met.tl_md}')

    ## Auto/Annual Booked
    df_aap = met.dfa
    met_aap = Metrics(df_aap)
    print(f'Auto Booked: {met_aap.tl_bk}')

    df_ma = met.dfm
    met_ma = Metrics(df_ma)
    print(f'Manual Booked: {met_ma.tl_bk}')
