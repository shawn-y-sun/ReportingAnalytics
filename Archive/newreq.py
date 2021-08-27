from Reporting import load_data, Print, brul3_a, Write, template_daily, template_scores
file_name = "Data/cibc_output_file_jun2018_to_sep2020.csv"
file_name = "Data/new_strat_noC_finalsysapproved_PTIflagremoved.xlsx"

if __name__ == "__main__":
    df = load_data(file_name)
    a = Print(df)
    a.time_frame(frame=(20200501, 20200630))
    a.show('scores')
