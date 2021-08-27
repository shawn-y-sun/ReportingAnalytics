from Reporting import load_data, Metrics, filter_new_brul3_before, filter_new_brul3_after, \
    filter_new_brul3_before_nopti, filter_new_brul3_after_nopti, st_pti_b

file_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\May - July 2021 patch 1.6 dataset Aug 3 DL.csv'

if __name__ == '__main__':
    df = load_data(file_path)
    met = Metrics(df, st_pti_b)
    met.time_frame(start=20210512, end=20210713)

    print('\nOverall')
    print(f'TTD: {met.tl_ttd}')
    print(f'TTD (ABC): {met.tl_ttdt}')

    print('\nWith PTI')
    print('\nWithout Strategy')
    met_before = met.copy()
    met_before.filter = filter_new_brul3_before
    met_before.apply_filter(False)
    print(f'Auto Approvals: {met_before.tl_aap}')
    print(f'Auto Approvals (ABC): {met_before.tl_aapt}')
    print(f'AutoApproval Amount: {met_before.tl_aap_ln}')
    print(f'AutoApproval Amount (ABC): {met_before.tl_aapt_ln}')

    print('\nWith Strategy')
    met_after = met.copy()
    met_after.filter = filter_new_brul3_after
    met_after.apply_filter(False)
    print(f'Auto Approvals: {met_after.tl_aap}')
    print(f'Auto Approvals (ABC): {met_after.tl_aapt}')
    print(f'AutoApproval Amount: {met_after.tl_aap_ln}')
    print(f'AutoApproval Amount (ABC): {met_after.tl_aapt_ln}')


    print('\nPTI Incremnetal')
    met_pti = met.copy()
    met_pti.strategy = st_pti_b
    met_pti.df = met_pti.df_incr_ttl
    print(f'Auto Approvals: {met_pti.tl_aap}')
    print(f'Auto Approvals (ABC): {met_pti.tl_aapt}')
    print(f'AutoApproval Amount: {met_pti.tl_aap_ln}')
    print(f'AutoApproval Amount (ABC): {met_pti.tl_aapt_ln}')








