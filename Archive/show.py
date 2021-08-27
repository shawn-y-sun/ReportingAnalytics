from Reporting import load_data, Print, brul3_a, Write, template_daily
import time

if __name__ == "__main__":
    start = time.time()

    df = load_data()
    a = Print(df, brul3_a)
    a.show('tr_ttd_pf')

    end = time.time()
    print(f'Runtime of the program is {end - start}')