import pandas as pd
from Reporting import load_data, Dataset
from tqdm import tqdm

if __name__ == '__main__':
    df_keys = pd.read_csv('reverse_decision_ids.csv')
    key_lst = df_keys['key'].tolist()
    df = load_data()
    ds = Dataset(df)
    ds.time_frame(start=20210301, end=20210831)
    ds_df = ds.df

    df_reversed = ds_df.copy()
    df_reversed_copy = df_reversed.copy()

    for index, row in tqdm(df_reversed_copy.iterrows()):
        if row['appseqno'] in key_lst:
            df_reversed.loc[index, 'final_decision'] = 'APPSCOR'
    
    print('Saving File ...')
    df_reversed.to_excel(r'C:\Users\sunsh\Documents\Daily Approval Report\Data\dataset_statusreversed.xlsx')

