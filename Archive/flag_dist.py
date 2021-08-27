from Reporting import load_data, Metrics
import pandas as pd

name_1 = 'EDH_202106'
name_2 = 'EDH_202006'
file_1 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\May - July 2021 patch 1.6 dataset Aug 3 DL.csv'
file_2 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\June 2020 - EDH 1.6.csv'
# Equifax Dataset if it is

if __name__ == '__main__':
    df_1 = load_data(file_1)
    df_2 = load_data(file_2)

    met1 = Metrics(df_1)
    met2 = Metrics(df_2)

    # Time Frame
    met1.time_frame(frame=(20210601, 20210630))
    met2.time_frame(frame=(20200601, 20200630))
    df1 = met1.df
    df2 = met2.df


    # Check for flags
    def flag_filter(para):
        if para[-4:].lower() == 'flag':
            return True
        else:
            return False

    column_lst1 = df1.columns.tolist()
    column_lst2 = df2.columns.tolist()

    flag_lst1 = list(filter(flag_filter, column_lst1))
    flag_lst2 = list(filter(flag_filter, column_lst2))


    # Get Distribution
    index_lst = []
    values_1 = []
    values_2 = []

    ttd1 = met1.tl_ttd
    ttd2 = met2.tl_ttd

    for flag in flag_lst2:
        flag_1 = flag.lower() if met2.external else flag
        flag_2 = flag
        
        ## Go through each dataset
        for comb in [(flag_1, df1, values_1, ttd1), (flag_2, df2, values_2, ttd2)]:
            flag_series = comb[1][comb[0]]
            
            # Map
            unique = flag_series.unique().tolist()

            if 'T' in unique or 'F' in unique:
                mapped = flag_series.map({'T': 1, 'F': 0})
                count = mapped.sum()
            elif 1 in unique or 0 in unique:
                count = flag_series.sum()
            
            elif flag_series.isnull().all():
                count = 0

            else:
                print(f'Error in {comb[0]}')
                continue

            comb[2].append(count / comb[3])
        
        index_lst.append(flag_1)

    ## Create DataFrame
    data = {name_1: values_1, name_2: values_2}
    df = pd.DataFrame(data, index = index_lst)
    df[f'Delta ({name_1}-{name_2})'] = df[name_1] - df[name_2]
    df.to_excel(f'flag_compare_{name_1}_{name_2}.xlsx')

    