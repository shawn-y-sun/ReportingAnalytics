from Reporting import load_data, Print

file_path1 = r'C:\Users\sunsh\Documents\EDH vs Equifax\July_2020_EDH.xlsx'
file_path2 = r'C:\Users\sunsh\Documents\Data\cibc_output_file_jun2018_to_sep2020.csv'

if __name__ == "__main__":
    # df1 = load_data(file_path1)
    # a = Print(df1)
    # a.show('dec_ttd')
    # a.show('tr_ttd')
    # a.show('sc_ttd')
    # a.show('sc_ttd_bni')

    print('----------------------------------------')

    df2 = load_data(file_path2)
    b = Print(df2)
    b.time_frame(start=20200701, end=20200701)
    b.show('dec_ttd')
    b.show('tr_ttd')
    # b.show('sc_ttd')
    # b.show('sc_ttd_bni')
