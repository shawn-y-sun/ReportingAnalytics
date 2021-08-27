import pandas as pd
import numpy as np
from Reporting import load_data

main_file = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\Sample - Equifax.xlsx'
booking_file = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\performance_all.xlsx'

df_main = load_data(main_file)
df_bookings = load_data(booking_file)

df_merged = df_main.merge(df_bookings, how='left', on='appseqno')
df_merged

df_merged.to_excel(r'Dataset_bookings.xlsx')