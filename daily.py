from Reporting import load_data, brul3_a, Write, template_daily

template_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\Artifact_Cumulative Report_Template.xlsx'
save_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report'
start_date = 20210512
end_date = None

if __name__ == "__main__":
    template_daily.file_name = template_path
    df = load_data()
    rp = Write(template_daily, df, brul3_a)
    rp.dir = save_path
    rp.time_frame(start=start_date)
    rp.time_frame(end=end_date)
    rp.write()
