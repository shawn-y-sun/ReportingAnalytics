import pandas as pd
import numpy as np
from .dataset import Dataset
from datetime import date, timedelta
from tqdm import tqdm
import functools
from functools import lru_cache
import copy
pd.options.mode.chained_assignment = None

class Metrics(Dataset):
    """A metrics Generator of a Dataset Obejct"""

    '''Scores keys'''
    s_keys = ['bcn9', 'bni', 'cscore']

    def __init__(self, dataset, strategy=None, filter=None):
        """Create a new Metrics object by inheriting the featurs from Dataset class"""
        super().__init__(dataset, strategy, filter)

    ## Total Metrics
    # TTD
    @property
    def tl_ttd(self):
        """Total TTD - All Tiers"""
        return self.df[self.p_key].nunique()

    @property
    def tl_ttdt(self):
        """Total TTD - Tier A B C"""
        return self.dft[self.p_key].nunique()

    # Auto Approved
    @property
    def tl_aap(self):
        """Total Auto Approved - All Tiers"""
        return self.dfa[self.p_key].nunique()

    @property
    def tl_aapt(self):
        """Total Auto Approved - Tier A B C"""
        return self.dfta[self.p_key].nunique()

    @property
    def tl_aap_r(self):
        """Total Auto Approval Rate - All Tiers"""
        return self.tl_aap / self.tl_ttd if self.tl_ttd != 0 else None

    @property
    def tl_aapt_r(self):
        """Total Auto Approval Rate - Tier A B C"""
        return self.tl_aapt / self.tl_ttd if self.tl_ttd != 0 else None
    
    # Manual Approved
    @property
    def tl_m(self):
        """Total Manual Approved - All Tiers"""
        return self.dfm[self.p_key].nunique()

    @property
    def tl_m_r(self):
        """Total Manual Approval Rate - All Tiers"""
        return self.tl_m / self.tl_ttd if self.tl_ttd != 0 else None
    
    @property
    def tl_mt(self):
        """Total Manual Approved - Tier A B C"""
        return self.dfmt[self.p_key].nunique()
    
    @property
    def tl_ma(self):
        """Total Manual Approved (Clean) - All Tiers"""
        return self.dfma[self.p_key].nunique()
    
    @property
    def tl_mc(self):
        """Total Manual Approved (Conditional) - All Tiers"""
        return self.dfmc[self.p_key].nunique()
    
    @property
    def tl_mat(self):
        """Total Manual Approved (Clean) - Tier A B C"""
        return self.dfmat[self.p_key].nunique()
    
    @property
    def tl_mct(self):
        """Total Manual Approved (Clean) - All Tiers"""
        return self.dfmct[self.p_key].nunique()
    
    # Declined
    @property
    def tl_d(self):
        """Total Declined - All Tiers"""
        return self.dfd[self.p_key].nunique()

    @property
    def tl_md(self):
        """Total Manual Declined - All Tiers"""
        return self.dfmd[self.p_key].nunique()
    
    @property
    def tl_ad(self):
        """Total Auto Declined - All Tiers"""
        return self.dfad[self.p_key].nunique()

    # Total Approved
    @property
    def tl_ap(self):
        """Total Approved (Auto + Manual) - All Tiers"""
        return self.tl_aap + self.tl_m
    
    @property
    def tl_ap_r(self):
        """Total Approval Rate (Auto + Manual) - All Tiers"""
        return self.tl_ap / self.tl_ttd

    ## Booked
    # All Booked
    @property
    def tl_bk(self):
        """Total Booked - All Tiers"""
        return self.dfbk[self.p_key].nunique()
    
    @property
    def tl_bkt(self):
        """Total Booked - Tier A B C"""
        return self.dfbkt[self.p_key].nunique()
    
    @property
    def tl_bkt_r(self):
        """Total Booking Rate - Tier A B C"""
        return self.tl_bkt / self.tl_ttd if self.tl_ttd != 0 else None
    
    # Auto Approved & Booked
    @property
    def tl_aap_bk(self):
        """Total Auto Approved then Booked - All Tiers"""
        return self.dfaap_bk[self.p_key].nunique()
    
    @property
    def tl_aapt_bk(self):
        """Total Auto Approved then Booked - Tier A B C"""
        return self.dfaapt_bk[self.p_key].nunique()

    # Manual Approved & Booked
    @property
    def tl_m_bk(self):
        """Total Manual Approved then Booked - All Tiers"""
        return self.dfm_bk[self.p_key].nunique()
    
    @property
    def tl_mt_bk(self):
        """Total Manual Approved then Booked - Tier A B C"""
        return self.dfmt_bk[self.p_key].nunique()
    
    # Manual Approved (Clean) & Booked
    @property
    def tl_ma_bk(self):
        """Total Manual Approved (Clean) then Booked - All Tiers"""
        return self.dfma_bk[self.p_key].nunique()
    
    # Manual Approved (Conditional) & Booked
    @property
    def tl_mc_bk(self):
        """Total Manual Approved (Conditional) then Booked - All Tiers"""
        return self.dfmc_bk[self.p_key].nunique()
    
    
    ## Bad
    @property
    def tl_bk_bd(self):
        """Total Booked and Bad Loans- All Tiers"""
        return self.dfbk_bd[self.p_key].nunique()

    
    ## Get rates
    def get_rates_helper(self, m1, m2, rates):
        """Helper function for get_rates()"""
        if m1 is None:
            return None

        if isinstance(m1, dict) and isinstance(m2, dict):
            rates_d = rates
            m1_d = m1
            m2_d = m2
            for key, val in m1_d.items():
                if isinstance(val, (int, float)):
                    if m2_d[key]==0:
                        rates_d[key] = 0
                    else:
                        rates_d[key] = m1_d[key] / m2_d[key]
                elif isinstance(val, pd.DataFrame):
                    rates_d[key] = m1_d[key].div(m2_d[key])
                    rates_d[key].replace(np.nan, 0, inplace=True)
                elif isinstance(val, dict):
                    rates_d[key] = {}
                    rates_d = rates_d[key]
                    m1_d = m1_d[key]
                    m2_d = m2_d[key]
                    self.get_rates_helper(m1_d, m2_d, rates_d)

    def get_rates(self, m1, m2):
        """Function to divide two dictionaries or dataframes with same keys

        :param m1: dictionary or dataframes as numerator
        :param m2: dictionary or dataframes as denominator
        :return: the ratios after division in the same format as m1 and m2
        """
        if m1 is None:
            return None

        rates = {}
        if isinstance(m1, dict) and isinstance(m2, dict):
            rates_d = rates
            m1_d = m1
            m2_d = m2
            for key, val in m1_d.items():
                if isinstance(val, (int, float)):
                    if m2_d[key]==0:
                        rates_d[key] = 0
                    else:
                        rates_d[key] = m1_d[key] / m2_d[key]
                elif isinstance(val, pd.DataFrame):
                    rates_d[key] = m1_d[key].div(m2_d[key])
                    rates_d[key].replace(np.nan, 0, inplace=True)
                elif isinstance(val, dict):
                    rates_d[key] = {}
                    rates_d = rates_d[key]
                    m1_d = m1_d[key]
                    m2_d = m2_d[key]
                    self.get_rates_helper(m1_d, m2_d, rates_d)

        return rates

    ## Tier Metrics
    def tiering(self, df, v_key=None, l_key='tier', mean=False, all_tiers=True, incl_total=False):
        """Create dictionary of count or values computation for each tier

        :param df: the dataframe
        :param v_key:set to the self defined variables name (refer to self.keys) 
            if it's a value you want to sum or average
        :param l_key: set to the numeric self defined variable name (refer to self.keys) 
            that the metrics should be segregated by (instead of tiers)
        :param mean: if v_key is numerical variable, set to True if you want the average, 
            False for sum
        :param all_tiers: when l_key is 'tier', set to True if you want to include tier F, N, 
            False for Tier A/B/C only
        :param incl_total: set True if you want to add values for total at first
        :return: the dictionary of metrics by tiers
        """
        if df is None:
            return None
        t_metrics = {}
        t_key = self.keys[l_key]
        v_key = self.keys[v_key] if self.keys.get(v_key, None) is not None else v_key
        
        if l_key != 'tier':
            vals = sorted(df[t_key].unique().tolist())
        else:
            if all_tiers:
                vals = ['A', 'B', 'C', 'F', 'N']
            else:
                vals = ['A', 'B', 'C']
        
        if incl_total:
            if v_key is None:
                t_metrics['Total'] = df[self.p_key].nunique()
            else:
                df_nodup = df.drop_duplicates(self.p_key)
                if mean:
                    t_metrics['Total'] = df_nodup[v_key].mean()
                else:
                    t_metrics['Total'] = df_nodup[v_key].sum()

        for v in vals:
            if v_key is None:
                t_metrics[f"{v}"] = df[df[t_key]==v][self.p_key].nunique()
            else:
                df_nodup = df.drop_duplicates(self.p_key)
                if mean:
                    t_metrics[f"{v}"] = df_nodup[df_nodup[t_key]==v][v_key].mean()
                else:
                    t_metrics[f"{v}"] = df_nodup[df_nodup[t_key]==v][v_key].sum()

        return t_metrics
    
    # ttd
    @property
    def tr_ttd(self):
        """TTD by tiers - all tiers"""
        return self.tiering(self.df)
    
    @property
    def tr_ttdt(self):
        """TTD by tiers - tier ABC"""
        return self.tiering(self.dft, all_tiers=False)
    
    # Auto approved
    @property
    def tr_aap(self):
        """Auto Approved by tiers - all tiers"""
        return self.tiering(self.dfa)
    
    @property
    def tr_aap_r(self):
        """Auto Approval Rate by tiers - all tiers"""
        return self.get_rates(self.tr_aap, self.tr_ttd)
    
    @property
    def tr_aapt(self):
        """Auto Approved by tiers - tier ABC"""
        return self.tiering(self.dfat, all_tiers=False)
    
    @property
    def tr_aapt_r(self):
        """Auto Approval Rate by tiers - tier ABC"""
        return self.get_rates(self.tr_aapt, self.tr_ttdt)

    # Manual Approved
    @property
    def tr_m(self):
        '''Total Manual Approved'''
        return self.tiering(self.dfm)

    @property
    def tr_m_r(self):
        return self.get_rates(self.tr_m, self.tr_ttd)

    @property
    def tr_mt(self):
        '''Manual Approved: Tier A, B, C'''
        return self.tiering(self.dfmt, all_tiers=False)
    
    @property
    def tr_ma(self):
        '''Manual Approved (clean): All tiers'''
        return self.tiering(self.dfma)

    @property
    def tr_mat(self):
        '''Manual Approved (clean): Tier A, B, C'''
        return self.tiering(self.dfmat, all_tiers=False)
    
    @property
    def tr_mc(self):
        '''Manual Approved (conditional): All tiers'''
        return self.tiering(self.dfmc)

    @property
    def tr_mct(self):
        '''Manual Approved (conditional): Tier A, B, C'''
        return self.tiering(self.dfmct, all_tiers=False)

    # Decline
    @property
    def tr_dt(self):
        '''All Declined: Tier A, B, C'''
        return self.tiering(self.dfdt, all_tiers=False)

    # Auto Decline
    @property
    def tr_ad(self):
        '''Auto Declined: all Tiers'''
        return self.tiering(self.dfad)

    @property
    def tr_adt(self):
        '''Auto Declined: Tier A, B, C'''
        return self.tiering(self.dfadt, all_tiers=False)
    
    # Manual Decline
    @property
    def tr_md(self):
        '''Manual Declined: All Tiers'''
        return self.tiering(self.dfmd)

    @property
    def tr_mdt(self):
        '''Manual Declined: Tier A, B, C'''
        return self.tiering(self.dfmdt, all_tiers=False)

    ## Booked
    # All Booked
    @property
    def tr_bk(self):
        '''All booked'''
        return self.tiering(self.dfbk)
    
    @property
    def tr_bkt(self):
        '''Booked: Tier A, B, C'''
        return self.tiering(self.dfbkt, all_tiers=False)
    
    @property
    def tr_bkt_r(self):
        '''Booked: Tier A, B, C'''
        return self.get_rates(self.tr_bkt, self.tr_ttdt)
    
    # Auto Approved & Booked
    @property
    def tr_aap_bk(self):
        return self.tiering(self.dfaap_bk)
    
    @property
    def tr_aapt_bk(self):
        return self.tiering(self.dfaapt_bk)
    
    @property
    def tr_aap_bk_r(self):
        return self.get_rates(self.tr_aap_bk, self.tr_aap)
    
    # Manual Approved & Booked
    @property
    def tr_m_bk(self):
        return self.tiering(self.dfm_bk)
    
    @property
    def tr_mt_bk(self):
        return self.tiering(self.dfmt_bk)
    
    @property
    def tr_m_bk_r(self):
        return self.get_rates(self.tr_m_bk_r, self.tr_m)
    
    # Manual Approved (Clean) & Booked
    @property
    def tr_ma_bk(self):
        return self.tiering(self.dfma_bk)
    
    # Manual Approved (Conditional) & Booked
    @property
    def tr_mc_bk(self):
        return self.tiering(self.dfmc_bk)


    ## Scores metrics
    def scoring(self, df_score, s_key='bcn9', _range=(400,1000), bins=50, 
                v_key=None, tiers=True, all_tiers=True):
        '''Function: create dict of scoring distribution'''
        if df_score is None or df_score.empty:
            return None
        
        if s_key == 'bni':
            _range = (500 , 1000)
        elif s_key == 'bcn9':
            _range = (350 , 900)
        elif s_key == 'cscore':
            _range = (300, 900)
        
        key = self.keys[s_key]
        p_key = self.p_key if v_key is None else self.keys[v_key]
        t_key = self.keys['tier']

        buckets = np.linspace(_range[0], _range[1], ((_range[1]-_range[0])//bins + 1))
        df_score.loc[:, "Buckets"] = pd.cut(df_score[key], buckets, right=True, include_lowest=False)

        # Distribution on total
        output = {}

        if v_key is None:
            result = pd.DataFrame(df_score.groupby("Buckets")[p_key].nunique())
        else:
            df_score_nodup = df_score.drop_duplicates(self.p_key)
            result = pd.DataFrame(df_score_nodup.groupby("Buckets")[p_key].sum())
        result.index.name = None
        result.rename(columns={p_key: "Count"}, inplace=True)
        result.replace(np.nan, 0, inplace=True)
        output['Total'] = result

        if not tiers:
            return output
        else:
            pass
        # Distribution on tiers
        df_score[t_key] = df_score[t_key].astype(str)
        tiers = ['A', 'B', 'C', 'F', 'N'] if all_tiers else ['A', 'B', 'C']
        for t in tiers:
            if df_score[df_score[t_key] == t].empty:
                output[f"Tier {t}"] = None
            else:
                if v_key is None:
                    result = pd.DataFrame(df_score[df_score[t_key] == t].\
                                        groupby("Buckets")[p_key].nunique())
                else:
                    df_score_nodup = df_score.drop_duplicates(self.p_key)
                    result = pd.DataFrame(df_score_nodup[df_score[t_key] == t].\
                                        groupby("Buckets")[p_key].sum())
                result.index.name = None
                result.rename(columns={p_key: "Count"}, inplace=True)
                result.replace(np.nan, 0, inplace=True)
                output[f"Tier {t}"] = result

        return output

    # TTD
    @property
    def sc_ttd(self):
        '''Dictionary of Scores Dists: TTD (all tiers)'''
        return self.scoring(self.df)
    
    @property
    def sc_ttdt(self):
        '''Dictionary of Scores Dists: TTD (Tier A B C)'''
        return self.scoring(self.dft, all_tiers=False)
    
    @property
    def bni_ttd(self):
        '''Dictionary of Scores Dists: TTD (all tiers)'''
        return self.scoring(self.df, s_key='bni')
    
    @property
    def cs_ttd(self):
        '''Dictionary of Scores Dists: TTD (all tiers)'''
        return self.scoring(self.df, s_key='cscore')

    # Auto Approved
    @property
    def sc_aap(self):
        '''Dictionary of Scores Dists: auto-approved (All tiers)'''
        return self.scoring(self.dfa)

    @property
    def sc_aapt(self):
        '''Dictionary of Scores Dists: auto-approved (Tier A B C)'''
        return self.scoring(self.dfat, all_tiers=False)
    
    @property
    def sc_aapt_r(self):
        '''Dictionary of Scores Dists: auto-approved rates (Tier A B C)'''
        return self.get_rates(self.sc_aapt, self.sc_ttdt)
    
    @property
    def bni_aap(self):
        '''Dictionary of Scores Dists: auto-approved (All tiers)'''
        return self.scoring(self.dfa, s_key='bni')
    
    @property
    def cs_aap(self):
        '''Dictionary of Scores Dists: auto-approved (All tiers)'''
        return self.scoring(self.dfa, s_key='cscore')
    
    # Manual Approved
    @property
    def sc_m(self):
        '''Dictionary of Scores Dists: manual approved (All tiers)'''
        return self.scoring(self.dfm)
    
    @property
    def bni_m(self):
        '''Dictionary of Scores Dists: manual approved (All tiers)'''
        return self.scoring(self.dfm, s_key='bni')
    
    @property
    def cs_m(self):
        '''Dictionary of Scores Dists: manual approved (All tiers)'''
        return self.scoring(self.dfm, s_key='cscore')

    @property
    def sc_mt(self):
        '''Dictionary of Scores Dists: manual approved (Tier A B C)'''
        return self.scoring(self.dfmt, all_tiers=False)
    
    @property
    def sc_ma(self):
        '''Dictionary of Scores Dists: manual approved (clean) (All tiers)'''
        return self.scoring(self.dfma)
    
    @property
    def bni_ma(self):
        '''Dictionary of Scores Dists: manual approved (clean) (All tiers)'''
        return self.scoring(self.dfma, s_key='bni')
    
    @property
    def cs_ma(self):
        '''Dictionary of Scores Dists: manual approved (clean) (All tiers)'''
        return self.scoring(self.dfma, s_key='cscore')

    @property
    def sc_mat(self):
        '''Dictionary of Scores Dists: manual approved (clean) (Tier A B C)'''
        return self.scoring(self.dfmat, all_tiers=False)
    
    @property
    def sc_mc(self):
        '''Dictionary of Scores Dists: manual approved (conditional) (All tiers)'''
        return self.scoring(self.dfmc)
    
    @property
    def bni_mc(self):
        '''Dictionary of Scores Dists: manual approved (conditional) (All tiers)'''
        return self.scoring(self.dfmc, s_key='bni')
    
    @property
    def cs_mc(self):
        '''Dictionary of Scores Dists: manual approved (conditional) (All tiers)'''
        return self.scoring(self.dfmc, s_key='cscore')

    @property
    def sc_mct(self):
        '''Dictionary of Scores Dists: manual approved (conditional) (Tier A B C)'''
        return self.scoring(self.dfmct, all_tiers=False)
    
    # Declined
    @property
    def sc_mdt(self):
        '''Dictionary of Scores Dists: manual declined (Tier A B C)'''
        return self.scoring(self.dfmdt, all_tiers=False)


    ## Booked
    # All Booked
    @property
    def sc_bk(self):
        '''Dictionary of Scores Dists: booked (All tiers)'''
        return self.scoring(self.dfbk)
    
    @property
    def bni_bk(self):
        '''Dictionary of Scores Dists: booked (All tiers)'''
        return self.scoring(self.dfbk, s_key='bni')
    
    @property
    def cs_bk(self):
        '''Dictionary of Scores Dists: booked (All tiers)'''
        return self.scoring(self.dfbk, s_key='cscore')
    
    @property
    def sc_bkt(self):
        '''Dictionary of Scores Dists: booked (Tier A B C)'''
        return self.scoring(self.dfbkt, all_tiers=False)
    
    @property
    def sc_bkt_r(self):
        '''Dictionary of Scores Dists: booked (Tier A B C)'''
        return self.get_rates(self.sc_bkt, self.sc_ttdt)

    # Auto Approved & Booked
    @property
    def sc_aap_bk(self):
        return self.scoring(self.dfaap_bk)
    
    @property
    def bni_aap_bk(self):
        '''Dictionary of Scores Dists: AA & booked (All tiers)'''
        return self.scoring(self.dfaap_bk, s_key='bni')
    
    @property
    def cs_aap_bk(self):
        '''Dictionary of Scores Dists: AA & booked (All tiers)'''
        return self.scoring(self.dfaap_bk, s_key='cscore')
    
    # Manual Approved & Booked
    @property
    def sc_m_bk(self):
        return self.scoring(self.dfm_bk)
    
    @property
    def bni_m_bk(self):
        '''Dictionary of Scores Dists: M & booked (All tiers)'''
        return self.scoring(self.dfm_bk, s_key='bni')
    
    @property
    def cs_m_bk(self):
        '''Dictionary of Scores Dists: M & booked (All tiers)'''
        return self.scoring(self.dfm_bk, s_key='cscore')
    
    # Manual Approved (Clean) & Booked
    @property
    def sc_ma_bk(self):
        return self.scoring(self.dfma_bk)
    
    @property
    def bni_ma_bk(self):
        '''Dictionary of Scores Dists: MA & booked (All tiers)'''
        return self.scoring(self.dfma_bk, s_key='bni')
    
    @property
    def cs_ma_bk(self):
        '''Dictionary of Scores Dists: MA & booked (All tiers)'''
        return self.scoring(self.dfma_bk, s_key='cscore')
    
    # Manual Approved (Conditional) & Booked
    @property
    def sc_mc_bk(self):
        return self.scoring(self.dfmc_bk)
    
    @property
    def bni_mc_bk(self):
        '''Dictionary of Scores Dists: MC & booked (All tiers)'''
        return self.scoring(self.dfmc_bk, s_key='bni')
    
    @property
    def cs_mc_bk(self):
        '''Dictionary of Scores Dists: MC & booked (All tiers)'''
        return self.scoring(self.dfmc_bk, s_key='cscore')


    ### Loan Metrics
    ## Approved loan amount
    # TTD
    @property
    def tl_ttd_ln(self):
        """Loan Amount: ttd (all tiers)"""
        return self.df.drop_duplicates(self.p_key)[self.keys['ap_amt']].sum()
    
    @property
    def tr_ttd_ln(self):
        """Loan Amount: tiers of ttd (all tiers)"""
        return self.tiering(self.df, v_key = 'ap_amt')

    @property
    def sc_ttd_ln(self):
        """Loan Amount: score bands of ttd (all tiers)"""
        return self.scoring(self.df, v_key = 'ap_amt')

    # Auto approved
    @property
    def tl_aap_ln(self):
        """Loan Amount: total of auto approved (all tiers)"""
        df_nodup = self.dfa.drop_duplicates(self.p_key)
        return df_nodup[self.keys['ap_amt']].sum()
    
    @property
    def tl_aapt_ln(self):
        """Loan Amount: total of auto approved (ABC)"""
        df_nodup = self.dfat.drop_duplicates(self.p_key)
        return df_nodup[self.keys['ap_amt']].sum()
    
    @property
    def tr_aap_ln(self):
        """Loan Amount: tiers of auto approved (all tiers)"""
        return self.tiering(self.dfa, v_key = 'ap_amt')

    @property
    def sc_aap_ln(self):
        """Loan Amount: score bands of auto approved (all tiers)"""
        return self.scoring(self.dfa, v_key = 'ap_amt')
    
    # Booked
    @property
    def tl_bk_ln(self):
        """Loan Amount: total of booked (all tiers)"""
        return self.dfbk.drop_duplicates(self.p_key)[self.keys['ap_amt']].sum()
    
    @property
    def tr_bk_ln(self):
        """Loan Amount: tiers of booked (all tiers)"""
        return self.tiering(self.dfbk, v_key = 'ap_amt')
    
    @property
    def tr_bkt_ln(self):
        """Loan Amount: tiers of booked (Tier A B C)"""
        return self.tiering(self.dfbkt, v_key = 'ap_amt', all_tiers=False)

    @property
    def sc_bk_ln(self):
        """Loan Amount: score bands of booked (all tiers)"""
        return self.scoring(self.dfbk, v_key = 'ap_amt')
    
    # Auto approved - Booked
    @property
    def tl_aap_bk_ln(self):
        """Loan Amount: total of auto approved and booked (all tiers)"""
        return self.dfaap_bk.drop_duplicates(self.p_key)[self.keys['ap_amt']].sum()
    
    @property
    def tr_aap_bk_ln(self):
        """Loan Amount: tiers of auto approved and booked (all tiers)"""
        return self.tiering(self.dfaap_bk, v_key = 'ap_amt')

    @property
    def sc_aap_bk_ln(self):
        """Loan Amount: score bands of auto approved and booked (all tiers)"""
        return self.scoring(self.dfaap_bk, v_key = 'ap_amt')

    ## Balance
    # Booked Bad Loans
    @property
    def tl_bk_bd_bal(self):
        """Balance: total of booked (all tiers)"""
        return self.dfbk_bd.drop_duplicates(self.p_key)[self.keys['balance']].sum()
    
    @property
    def tr_bk_bd_bal(self):
        """Balance: tiers of booked (all tiers)"""
        return self.tiering(self.dfbk_bd, v_key = 'balance')
    
    @property
    def tr_bkt_bd_bal(self):
        """Balance: tiers of booked (Tier A B C)"""
        return self.tiering(self.dfbkt_bd, v_key = 'balance', all_tiers=False)

    @property
    def sc_bk_bd_bal(self):
        """Balance: score bands of booked (all tiers)"""
        return self.scoring(self.dfbk_bd, v_key = 'balance')

    # Auto approved & Booked Bad Loans
    @property
    def tl_aap_bk_bd_bal(self):
        """Balance: total of auto approved and booked (all tiers)"""
        return self.dfaap_bk_bd.drop_duplicates(self.p_key)[self.keys['balance']].sum()
    
    @property
    def tr_aap_bk_bd_bal(self):
        """Balance: tiers of auto approved and booked (all tiers)"""
        return self.tiering(self.dfaap_bk_bd, v_key = 'balance')

    @property
    def sc_aap_bk_bd_bal(self):
        """Balance: score bands of auto approved and booked (all tiers)"""
        return self.scoring(self.dfaap_bk_bd, v_key = 'balance')
    
    ## Bad Rates
    # Booked Bad Loans
    @property
    def tl_bk_bd_r(self):
        """Bad Rates: total of booked (all tiers)"""
        if self.tl_bk_ln == 0:
            return 0
        else:
            return self.tl_bk_bd_bal / self.tl_bk_ln
    
    @property
    def tr_bk_bd_r(self):
        """Bad Rates: tiers of booked (all tiers)"""
        return self.get_rates(self.tr_bk_bd_bal, self.tr_bk_ln)
    
    @property
    def tr_bkt_bd_r(self):
        """Bad Rates: tiers of booked (Tier A B C)"""
        return self.get_rates(self.tr_bkt_bd_bal, self.tr_bkt_ln)
    
    @property
    def sc_bk_bd_r(self):
        """Bad Rates: score bands of booked (all tiers)"""
        return self.get_rates(self.sc_bk_bd_bal, self.sc_bk_ln)
    
    # Auto approved & Booked Bad Loans
    @property
    def tl_aap_bk_bd_r(self):
        """Bad Rates: total of auto approved booked (all tiers)"""
        return self.tl_aap_bk_bd_bal / self.tl_aap_bk_ln
    
    @property
    def tr_aap_bk_bd_r(self):
        """Bad Rates: tiers of auto approved booked (all tiers)"""
        return self.get_rates(self.tr_aap_bk_bd_bal, self.tr_aap_bk_ln)
    
    @property
    def sc_aap_bk_bd_r(self):
        """Bad Rates: score bands of auto approved booked (all tiers)"""
        return self.get_rates(self.sc_aap_bk_bd_bal, self.sc_aap_bk_ln)


    ### Strat Metrics
    ## Total/Tier Level
    # All Incremental
    @property
    def tl_incr(self):
        """Total number"""
        if self.strategy is None:
            return None

        return self.df_incr_ttl[self.p_key].nunique()
        

    @property
    def tr_incr(self):
        """Tier numbers"""
        return self.tiering(self.df_incr_ttl)
    
    # Incremental: Auto Approved
    @property
    def tl_incr_aap(self):
        """Total number"""
        if self.strategy is None:
            return None

        return self.df_incr_aapt_ttl[self.p_key].nunique()

    @property
    def tr_incr_aap(self):
        """Tier numbers"""
        return self.tiering(self.df_incr_aapt_ttl, all_tiers=False)

    # Violation
    @property
    def tl_vlt(self):
        """Total number"""
        if self.strategy is None or self.vlt is None:
            return None

        return self.df_vlt_ttl[self.p_key].nunique()

    @property
    def tr_vlt(self):
        """Tier numbers"""
        return self.tiering(self.df_vlt_ttl)
    
    # Incremental Performance: Approved Loan
    @property
    def tl_incr_ttd_ln(self):
        """Total Approved Loan: Incremental TTD"""
        incr_metric = Metrics(self.df_incr_ttl)
        return incr_metric.tl_ttd_ln
    
    @property
    def tl_incr_aap_ln(self):
        """Total Approved Loan: Incremental Auto Approved"""
        incr_metric = Metrics(self.df_incr_ttl)
        return incr_metric.tl_aap_ln

    # Incremental Performance: Booked Loan
    @property
    def tl_incr_bk_ln(self):
        """Total Booked Loan: Incremental Booked"""
        incr_metric = Metrics(self.df_incr_ttl)
        return incr_metric.tl_bk_ln

    
    ## Strategy-level
    # All Incremental
    @property
    def incr(self):
        '''TTD'''
        if self.df_incr is None:
            return None
        metrics = {}
        for key, ds in self.df_incr.items():
            metrics[key] = self.tiering(ds)
        
        return metrics

    # Incremental: Auto Approved
    @property
    def incr_aapt(self):
        if self.df_incr_aapt is None:
            return None
        metrics = {}
        for key, ds in self.df_incr_aapt.items():
            metrics[key] = self.tiering(ds, all_tiers=False)
        
        return metrics


    # Violation
    @property
    def vlt(self):
        if self.df_vlt is None:
            return None
        metrics = {}
        for key, ds in self.df_vlt.items():
            metrics[key] = self.tiering(ds)
        
        return metrics
    
    ## Strategy Delta
    # Bad Rates
    @property
    def dlt_bk_bd_r(self):
        if self.df_delta is None:
            return None
        metrics = {}
        for key, dfs in self.df_delta.items():
            df_in= dfs['in']
            df_out = dfs['out']
            metrics[key] = {}

            ## Get bad rates
            met_in = Metrics(df_in)
            met_out = Metrics(df_out)
            metrics[key]['in'] = met_in.tl_bk_bd_r
            metrics[key]['out'] = met_out.tl_bk_bd_r
        
        return metrics

    ## Create dict for metrics
    # Total metrics
    @property
    def total(self):
        metrics = {}
        metrics['TTD'] = self.tl_ttd

        metrics['Auto Approved (all tiers)'] = self.tl_aap
        metrics['Auto Approved'] = self.tl_aapt
        metrics['Auto Approval Rate'] = self.tl_aapt_r

        metrics['Manual Approved (all tiers)'] = self.tl_m
        metrics['Manual Approved'] = self.tl_mt
        metrics['Manual Approved (clean) (all tiers)'] = self.tl_ma
        metrics['Manual Approved (conditional) (all tiers)'] = self.tl_mc
        metrics['Manual Approved (clean)'] = self.tl_mat
        metrics['Manual Approved (conditional)'] = self.tl_mct

        metrics['Booked (all tiers)'] = self.tl_bk
        metrics['Booked'] = self.tl_bkt
        metrics['Booking Rate'] = self.tl_bkt_r

        metrics['Incremental (All)'] = self.tl_incr
        metrics['Incremental (Auto Approved)'] = self.tl_incr_aap
        metrics['Violation'] = self.tl_vlt
        return metrics

    # Tier metrics
    @property
    def tier(self):
        metrics = {}
        metrics['TTD (all tiers)'] = self.tr_ttd
        metrics['TTD'] = self.tr_ttdt

        metrics['Auto Approved (all tiers)'] = self.tr_aap
        metrics['Auto Approved'] = self.tr_aapt
        metrics['Auto Approved Rates'] = self.tr_aapt_r

        metrics['Manual Approved (all tiers)'] = self.tr_m
        metrics['Manual Approved'] = self.tr_mt
        metrics['Manual Approved (clean) (all tiers)'] = self.tr_ma
        metrics['Manual Approved (conditional) (all tiers)'] = self.tr_mc
        metrics['Manual Approved (clean)'] = self.tr_mat
        metrics['Manual Approved (conditional)'] = self.tr_mct

        metrics['Booked (all tiers)'] = self.tr_bk
        metrics['Booked'] = self.tr_bkt
        metrics['Booked Rates'] = self.tr_bkt_r

        metrics['Incremental'] = self.tr_incr
        metrics['Incremental (Auto Approved)'] = self.tr_incr_aap
        metrics['Violation'] = self.tr_vlt
        return metrics

    # Scores metrics
    @property
    def scores(self):
        metrics = {}
        metrics['TTD (all tiers)'] = self.sc_ttd
        metrics['TTD'] = self.sc_ttdt

        metrics['Auto Approved (all tiers)'] = self.sc_aap
        metrics['Auto Approved'] = self.sc_aapt
        metrics['Auto Approved Rates'] = self.sc_aapt_r

        metrics['Manual Approved (all tiers)'] = self.sc_m
        metrics['Manual Approved'] = self.sc_mt
        metrics['Manual Approved (clean) (all tiers)'] = self.sc_ma
        metrics['Manual Approved (conditional) (all tiers)'] = self.sc_mc
        metrics['Manual Approved (clean)'] = self.sc_mat
        metrics['Manual Approved (conditional)'] = self.sc_mct

        metrics['Booked (all tiers)'] = self.sc_bk
        metrics['Booked'] = self.sc_bkt
        metrics['Booked Rates'] = self.sc_bkt_r

        return metrics

    
    ## All Metrics
    @property
    def all(self):
        return {'Total Metrics': self.total,
                'Tier Metrics': self.tier,
                'Incremental Metrics': self.incr,
                'Incremental Metrics (Auto Approved Tier ABC)': self.incr_aapt,
                'Violation Metrics': self.vlt}
    
    ## Profiles
    @property
    def profile_items(self):
        profile_items_1 = ['uw76_income', 'bcn9', 'bni', 'cscore']
        profile_items_2 = ['uw21_ltv', 'uw57_pti', 'uw58_tdsr', 'uw48_cbage', 'uw49_ot']
        profile_items_3 = ['uw20_activetrades', 'uw22_3rtrades', 'uw55_badtrades',
                            'uw8_bib', 'uw192_cald', 'uw34_bir']
        profile_items_4 = ['bad rates']
        profile_items = profile_items_1 + profile_items_2 + profile_items_3 + profile_items_4
        return profile_items

    def convert_bool(self, df):
        df_converted = df.copy()
        columns = df_converted.columns.tolist()
        for col in columns:
            if set(df_converted[col].dropna().tolist()).issubset(set(['T', 'F'])):
                df_converted[col] = np.where(df_converted[col]=='T', 1, df_converted[col])
                df_converted[col] = np.where(df_converted[col]=='F', 0, df_converted[col])

        return df_converted
    
    @property
    def outlier_dict(self):
        item = {
            'uw21_ltv': (0, 300),
            'uw57_pti': (0, 300),
            'uw58_tdsr': (0, 2000)
        }
        return item
    
    def filter_outliers(self, df):
        df_processed = df.copy()

        for key, _range in self.outlier_dict.items():
            key_act = self.keys[key]
            lowerbound = _range[0]
            upperbound = _range[1]

            df_processed[key_act] = np.where(df_processed[key_act]<lowerbound,
                                            lowerbound, df_processed[key_act])
            
            df_processed[key_act] = np.where(df_processed[key_act]>upperbound,
                                            upperbound, df_processed[key_act])

        return df_processed

    @lru_cache(maxsize=5)
    def get_mean(self, df, key):
        v_key = key if self.keys.get(key, None) is None else self.keys[key]
        df_nodup = df.drop_duplicates(self.p_key)
        return df_nodup[v_key].mean()
    
    @lru_cache(maxsize=5)
    def get_profiles_total(self, df_name, calc='mean'):
        profile_df = self.convert_bool(getattr(self, df_name))
        profiles = {}
        for item in self.profile_items:
            if item == 'bad rates':
                pass

            else:
                if calc == 'mean':
                    profiles[item] = self.get_mean(profile_df, item)
        
        return profiles

    @lru_cache(maxsize=5)
    def get_profiles_tier(self, df_name, calc='mean', all_tiers=False, filter_outliers=True, incl_total=True):
        profile_df = self.convert_bool(getattr(self, df_name))
        if filter_outliers:
            profile_df = self.filter_outliers(profile_df)

        profiles = {}
        for item in self.profile_items:
            if item == 'bad rates':
                met = Metrics(profile_df)
                profiles[item] = {}
                if incl_total:
                    profiles[item]['Total'] = met.tl_bk_bd_r
                profiles[item].update(met.tr_bkt_bd_r)

            else:
                mean_bool = True if calc == 'mean' else False
                profiles[item] = self.tiering(profile_df, v_key=item, 
                                                mean=mean_bool, all_tiers=all_tiers, incl_total=incl_total)

        return profiles
    
    # Total Profiles
    @property
    def tl_ttd_pf(self):
        return self.get_profiles_total('df')
    

    # Tier Profiles (Tier A B C)
    @property
    def tr_ttdt_pf(self):
        return self.get_profiles_tier('dft')
    
    @property
    def tr_aapt_pf(self):
        return self.get_profiles_tier('dfat')
    
    @property
    def tr_mt_pf(self):
        return self.get_profiles_tier('dfmt')
    
    @property
    def tr_mat_pf(self):
        return self.get_profiles_tier('dfmat')
    
    @property
    def tr_mct_pf(self):
        return self.get_profiles_tier('dfmct')
    
    @property
    def tr_adt_pf(self):
        return self.get_profiles_tier('dfadt')
    
    @property
    def tr_mdt_pf(self):
        return self.get_profiles_tier('dfmdt')
    
    @property
    def tr_dt_pf(self):
        return self.get_profiles_tier('dfdt')
    
    @property
    def tr_bkt_pf(self):
        return self.get_profiles_tier('dfaapt_bk')

    @property
    def tr_aapt_bk_pf(self):
        return self.get_profiles_tier('dfaapt_bk')
    
    @property
    def tr_mt_bk_pf(self):
        return self.get_profiles_tier('dfmt_bk')
    
        
    ## Other Metrics
    @property
    def csg_ttd(self):
        return self.tiering(self.df, l_key='cs_seg')
    
    @property
    def dec_ttd(self):
        return self.tiering(self.df, l_key='status')
    
    @property
    def sc_ttd_bni(self):
        return self.scoring(self.df, s_key='bni')
    
    @property
    def sc_aap_bni(self):
        return self.scoring(self.dfa, s_key='bni')


    ## Get Timely Metrics
    # Get Monthly Metrics
    @lru_cache(maxsize=5)
    def get_monthly(self, metric, mtype=None):
        monthly_dfs = self.monthly_dfs

        mly_metrics = {}
        for month, df in monthly_dfs.items():
            m = Metrics(df, self.strategy)
            if mtype:
                mly_metrics[month] = getattr(m, mtype)[metric]
            else:
                mly_metrics[month] = getattr(m, metric)
            
        return mly_metrics
    
    # Get Yearly Metrics
    @lru_cache(maxsize=5)
    def get_yearly(self, metric, fiscal=False, mtype=None):
        yearly_dfs = self.yearly_dfs if not fiscal else self.f_yearly_dfs

        yly_metrics = {}
        for year, df in yearly_dfs.items():
            m = Metrics(df, self.strategy)
            if mtype:
                yly_metrics[year] = getattr(m, mtype)[metric]
            else:
                yly_metrics[year] = getattr(m, metric)
        
        return yly_metrics
    
    # Get monthly metrics in all years
    @lru_cache(maxsize=5)
    def get_yearly_monthly(self, metric, fiscal=False, mtype=None):
        yearly_monthly_dfs = self.yearly_monthly_dfs if not fiscal \
            else self.f_yearly_monthly_dfs

        yly_mly_metrics = {}
        for year, mths_dict in yearly_monthly_dfs.items():

            mly_metrics = {}
            for month, df in mths_dict.items():
                m = Metrics(df, self.strategy)
                if mtype:
                    mly_metrics[month] = getattr(m, mtype)[metric]
                else:
                    mly_metrics[month] = getattr(m, metric)
            
            yly_mly_metrics[year] = mly_metrics
        
        return yly_mly_metrics
