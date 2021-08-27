from Reporting import load_data, brul3_a, Write, template_scores

template_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\Score bands_New Template.xlsx'
save_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report'
start_date = 20210512
end_date = None

if __name__ == "__main__":
    template_scores.file_name = template_path
    df = load_data()
    rp = Write(template_scores, df, brul3_a)
    rp.dir = save_path
    rp.time_frame(start=start_date)
    rp.time_frame(end=end_date)
    rp.write()