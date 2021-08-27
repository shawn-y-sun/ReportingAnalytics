from Reporting import load_data, Metrics, brul3

last_dec = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_reporting.csv'
first_dec = r'C:\Users\sunsh\Documents\Daily Approval Report\Data\master dataset\master_reversed.csv'

if __name__ == "__main__":
    df_last = load_data(last_dec)
    df_first = load_data(first_dec)

    ## Last Decision
    print('\nLast Decision')
    
    met_last = Metrics(df_last, brul3)
    met_last.time_frame(frame=(20210512, 20210610))

    met_last_incr = met_last.copy()
    met_last_incr.df = met_last.df_incr_ttl

    print(f'Incremental Auto Approved #: {met_last_incr.tl_aap}')
    print(f'Incremental Auto Approved $:{met_last_incr.tl_aap_ln}')
    print(f'Incremental Booked #: {met_last_incr.tl_aap_bk}')
    print(f'Incremental Booked $:{met_last_incr.tl_aap_bk_ln}')


    # First Decision
    print('\nFirst Decision')
    
    met_first = Metrics(df_first, brul3)
    met_first.time_frame(frame=(20210512, 20210610))

    met_first_incr = met_first.copy()
    met_first_incr.df = met_first.df_incr_ttl

    met_first_incr = met_first.copy()
    met_first_incr.df = met_first.df_incr_ttl

    print(f'Incremental Auto Approved #: {met_first_incr.tl_aap}')
    print(f'Incremental Auto Approved $:{met_first_incr.tl_aap_ln}')
    print(f'Incremental Booked #: {met_first_incr.tl_aap_bk}')
    print(f'Incremental Booked $:{met_first_incr.tl_aap_bk_ln}')