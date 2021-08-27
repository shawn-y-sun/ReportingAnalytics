from Reporting import load_data, Print, st_pti_b

file_path1 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\July Dataset - Shrawan Report.xlsx'
file_path2 = r'C:\Users\sunsh\Documents\Data\cibc_output_file_jun2018_to_sep2020.csv'

if __name__ == "__main__":
    df1 = load_data(file_path1)
    a = Print(df1, st_pti_b).copy()
    a.time_frame(end=20210531)
    a.show('tl_ttd')
    a.show('tl_aap')
    a.show('tl_aap_r')
    a.df = a.df_incr_ttl
    a.show('tr_m')
