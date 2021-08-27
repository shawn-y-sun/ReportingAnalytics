from Reporting import load_data, Print, brul3_a, Write, template_daily, template_scores

if __name__ == "__main__":
    df = load_data()
    # a = Print(df, brul3_a)
    # a.show()
    print('*************************')
    print('Generating Report 1 ...')
    b = Write(template_daily, df, brul3_a)
    b.write()
    print('\n')
    print('Generating Report 2 ...')
    c = Write(template_scores, df, brul3_a)
    c.write()