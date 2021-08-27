from Reporting import load_data, Metrics

file1 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\New Dataset - May12July13_bookings_statusreversed.xlsx'
file2 = r'C:\Users\sunsh\Documents\Data\cibc_output_file_jun2018_to_sep2020.csv'

if __name__ == '__main__':
    df_edh = load_data(file1)
    df_equ = load_data(file2)

    met_2106 = Metrics(df_edh)
    met_2106.time_frame(frame=(20210601, 20210630))
    print(f'\nJune 2021')
    print(met_2106.tr_ttd)
    print(met_2106.tr_ttd_ln)

    met_2006 = Metrics(df_equ)
    met_2006.time_frame(frame=(20200601, 20200630))
    print(f'\nJune 2020')
    print(met_2006.tr_ttd)
    print(met_2006.tr_ttd_ln)

