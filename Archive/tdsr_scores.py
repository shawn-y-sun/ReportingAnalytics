from Reporting import load_data, Write, template_scores_tdsr

file_path = r'C:\Users\sunsh\Documents\TDSR A Decline\TDSRA_over65_makingitthrough_noTDSRrule.xlsx'
if __name__ == "__main__":
    df = load_data(file_path)

    print('Generating Report  ...')
    c = Write(template_scores_tdsr, df)
    c.write()