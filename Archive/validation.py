from Reporting import load_data, Metrics

master_file = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master.csv'
bench_210507 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\May - July 2021 patch 1.6 dataset Aug 3 DL.csv'
bench_2006 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\June 2020 - EDH 1.6_bookings.xlsx'

if __name__ == "__main__":
    df_master = load_data(master_file)
    df_210507 = load_data(bench_210507)
    df_2006 = load_data(bench_2006)

    met_mas = Metrics(df_master)
    met_ben_210507 = Metrics(df_210507)
    met_ben_2006 = Metrics(df_2006)

    ## May21 - July21 
    print('\nMay - July 2021')
    # Master
    met_mas_210507 = met_mas.copy()
    met_mas_210507.time_frame(frame=(20210501, 20210731))

    print('\n Master Dataset')
    print(f'TTD: {met_mas_210507.tr_ttd}')
    #print(f'TTD BCN: {met_mas_210507.sc_ttd}')
    print(f'AA: {met_mas_210507.tr_aap}')
    print(f'MA: {met_mas_210507.tr_ma}')
    print(f'MC: {met_mas_210507.tr_mc}')
    print(f'AD: {met_mas_210507.tr_ad}')
    print(f'MD: {met_mas_210507.tr_md}')

    # Bench
    met_ben_210507.time_frame(frame=(20210501, 20210731))

    print('\n Bench Dataset')
    print(f'TTD: {met_ben_210507.tr_ttd}')
    #print(f'TTD BCN: {met_ben_210507.sc_ttd}')
    print(f'AA: {met_ben_210507.tr_aap}')
    print(f'MA: {met_ben_210507.tr_ma}')
    print(f'MC: {met_ben_210507.tr_mc}')
    print(f'AD: {met_ben_210507.tr_ad}')
    print(f'MD: {met_ben_210507.tr_md}')

    ## June 2020
    print('\nJune 2020')
    # Master
    met_mas_2006 = met_mas.copy()
    met_mas_2006.time_frame(frame=(20200601, 20200630))

    print('\n Master Dataset')
    print(f'TTD: {met_mas_2006.tr_ttd}')
    #print(f'TTD BCN: {met_mas_210507.sc_ttd}')
    print(f'AA: {met_mas_2006.tr_aap}')
    print(f'MA: {met_mas_2006.tr_ma}')
    print(f'MC: {met_mas_2006.tr_mc}')
    print(f'AD: {met_mas_2006.tr_ad}')
    print(f'MD: {met_mas_2006.tr_md}')

    # Bench
    met_ben_2006.time_frame(frame=(20200601, 20200630))

    print('\n Bench Dataset')
    print(f'TTD: {met_ben_2006.tr_ttd}')
    #print(f'TTD BCN: {met_ben_2006.sc_ttd}')
    print(f'AA: {met_ben_2006.tr_aap}')
    print(f'MA: {met_ben_2006.tr_ma}')
    print(f'MC: {met_ben_2006.tr_mc}')
    print(f'AD: {met_ben_2006.tr_ad}')
    print(f'MD: {met_ben_2006.tr_md}')




    
