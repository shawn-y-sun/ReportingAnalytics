from Reporting import load_data
import pandas as pd
from tqdm import tqdm

file_path = r'C:\Users\sunsh\Documents\decision compare\2021_decisiondate.xlsx'
if __name__ == '__main__':
    df_decision = load_data()
    df_decision_nafilled = df_decision.copy()
    df_decision_nafilled['from_id_decisionid'].fillna(99999999, inplace=True)
    app_lst = list(set(df_decision_nafilled['appseqno'].tolist()))

    df_groupby = df_decision_nafilled.groupby('appseqno')
    sysapp_app = []
    for app in tqdm(app_lst):
        df_sub = df_groupby.get_group(app)
        
        min_decid = df_sub['from_id_decisionid'].min()
        max_decid = df_sub['from_id_decisionid'].max()
        
        first_decision = df_sub.loc[df_sub['from_id_decisionid']==min_decid, 'decisionstatus'].values[0]
        last_decision = df_sub.loc[df_sub['from_id_decisionid']==max_decid, 'decisionstatus'].values[0]
        
        if first_decision == 'APPSCOR' and last_decision!='APPSCOR':
            sysapp_app.append(app)
    
    df_keys = pd.DataFrame({'key':sysapp_app})
    df_keys.to_csv('reverse_decision_ids.csv')


    


