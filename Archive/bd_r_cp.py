from Reporting import load_data, Metrics
import time
import datetime

if __name__ == "__main__":

    file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_reporting.csv'
    df = load_data(file_name)
    met = Metrics(df)
    met.time_frame(frame=(20190801, 20200331))

    new_keys = met.keys
    new_keys['bk_status'] = 'bookingstatus'
    met.keys = new_keys

    new_vals = met.vals
    
    ## BOOKED
    new_vals['C_Booked'] = (2,)
    met.vals = new_vals
    
    print('\nBOOKED')
    print(f"C_Booked: {met.vals['C_Booked']}")
    # All
    print('\nAll')
    print(f'Overall: {met.tl_bk_bd_r}')
    print(f'Tier: {met.tr_bk_bd_r}')

    # Auto Approved
    print('\nAuto Approved')
    met_aa = met.copy()
    met_aa.df = met.dfa
    print(f'Overall: {met_aa.tl_bk_bd_r}')
    print(f'Tier: {met_aa.tr_bk_bd_r}')

    # Manual Approved
    print('\nManual Approved')
    met_m = met.copy()
    met_m.df = met.dfm
    print(f'Overall: {met_m.tl_bk_bd_r}')
    print(f'Tier: {met_m.tr_bk_bd_r}')

    # Manual Approved (Clean)
    print('\nManual Approved (Clean)')
    met_ma = met.copy()
    met_ma.df = met.dfma
    print(f'Overall: {met_ma.tl_bk_bd_r}')
    print(f'Tier: {met_ma.tr_bk_bd_r}')

    # Manual Approved (Conditional)
    print('\nManual Approved (Conditional)')
    met_mc = met.copy()
    met_mc.df = met.dfmc
    print(f'Overall: {met_mc.tl_bk_bd_r}')
    print(f'Tier: {met_mc.tr_bk_bd_r}')



    ## BOOKEX
    new_vals['C_Booked'] = (3,)
    met.vals = new_vals

    print('\nBOOKEX')
    print(f"C_Booked: {met.vals['C_Booked']}")
    # All
    print('\nAll')
    print(f'Overall: {met.tl_bk_bd_r}')
    print(f'Tier: {met.tr_bk_bd_r}')

    # Auto Approved
    print('\nAuto Approved')
    met_aa = met.copy()
    met_aa.df = met.dfa
    print(f'Overall: {met_aa.tl_bk_bd_r}')
    print(f'Tier: {met_aa.tr_bk_bd_r}')

    # Manual Approved
    print('\nManual Approved')
    met_m = met.copy()
    met_m.df = met.dfm
    print(f'Overall: {met_m.tl_bk_bd_r}')
    print(f'Tier: {met_m.tr_bk_bd_r}')

    # Manual Approved (Clean)
    print('\nManual Approved (Clean)')
    met_ma = met.copy()
    met_ma.df = met.dfma
    print(f'Overall: {met_ma.tl_bk_bd_r}')
    print(f'Tier: {met_ma.tr_bk_bd_r}')

    # Manual Approved (Conditional)
    print('\nManual Approved (Conditional)')
    met_mc = met.copy()
    met_mc.df = met.dfmc
    print(f'Overall: {met_mc.tl_bk_bd_r}')
    print(f'Tier: {met_mc.tr_bk_bd_r}')
    

