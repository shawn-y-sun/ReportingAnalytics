from Reporting import load_data, Write, st_tdsr, template_tdsr_dec
import time
import datetime
file_path = r'C:\Users\sunsh\Documents\TDSR A Decline\TDSRA_over65_makingitthrough_noTDSRrule.xlsx'

if __name__ == "__main__":
    start = time.time()
    ################################################
    
    df = load_data(file_path)
    # print(df.shape)
    # print('*************************')
    # print('Generating Report ...')
    # a = Write(template_tdsr_dec, df, st_tdsr)
    # print(a.df.shape)
    # a.time_frame(frame=(20180601, 20190831))
    # print(a.df.shape)
    # b = a.copy()
    # print(b.df.shape)
    # print(a.df_vlt_ttl.shape)
    # b.df = a.df_vlt_ttl
    # print(b.df.shape)
    # print(b.df['FINAL_DECISION'].unique())
    # print(b.df['UW58_ACT'].min())
    # b.write()
    a = Write(template_tdsr_dec, df)
    a.write()

    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'[Runtime of the program is {time_str}]')