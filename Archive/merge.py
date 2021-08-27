from Reporting import load_data
import pandas as pd

file1 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_202004-202008_reversed.xlsx'
file2 = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_202104-202108_reversed.xlsx'

if __name__ == "__main__":
    df1 = load_data(file1)
    df2 = load_data(file2)

    frames = [df1, df2]
    all_parts = pd.concat(frames)
    
    all_parts.to_csv(r'C:\Users\sunsh\Documents\Daily Approval Report\Data\dataset_merged.csv', index=False)