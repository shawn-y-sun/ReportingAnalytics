from Reporting import load_data, Write, template_new_fy_update_v5
import time
import datetime

template_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\New Report Template_v5.xlsx'
save_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report'

update_column_index = 'AL'
start_time = 20210801
end_time = 20210831

if __name__ == "__main__":
    start = time.time()

    ################################################
    template_new_fy_update_v5.file_name = template_path
    template_new_fy_update_v5.entries.move_all(col_ind = update_column_index, inplace=True)

    # Load New Data
    df = load_data()

    ## Monthly update
    rp = Write(template_new_fy_update_v5, df)
    rp.dir = save_path
    rp.time_frame(start=start_time, end=end_time)
    rp.write()

    ###############################################
    end = time.time()
    time_secs = end - start
    time_str = str(datetime.timedelta(seconds=time_secs))[:-4]
    print(f'[Runtime of the program is {time_str}]')