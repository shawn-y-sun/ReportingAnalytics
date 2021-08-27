import pandas as pd
import functools
import datetime
import copy

class Dataset:
    """A dataset and its variants in pandas dataframes format"""
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    f_months = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self, df, strategy=None, filter=None):
        """Create a new Dataset

        :param df: A pandas dataframe
        :param strategy: A Strategy object (default None)
        :param filter: A Filter object (default None)
        """
        self.df = df
        self.strategy = strategy
        self.filter = filter
        self._keys = {}
        self._vals = {}
    
    def copy(self):
        """Return a copy of itself"""
        return copy.deepcopy(self)

    @property
    def external(self):
        """Return True if the dataset in Equifax format"""
    
        ext_cols = ['EFX_CLIENT_INDEX', 'INITIATION_DT', 'CIBC_BOOKED_LOAN',
                    'BOOKED_LOAN', 'TIER', 'CUSTOM_SCORES', 'CUSTOM_SCORES_SEG',
                    'BCN9', 'BNI3', 'BALANCE', 'LOAN_AMOUNT', 'EFX_STATUS',
                    'WORST_RATING', 'FIRST_DECISION', 'FINAL_DECISION',
                    'APPROVED_AMOUNT_NUM', 'APPROVED_SELLING_PRICE_NUM',
                    'APPROVED_CASH_DOWN_NUM', 'APPROVED_NET_TRADE_IN_NUM',
                    'APPROVED_TOTAL_AMOUNT_FINANCED_NUM']

        return all([col in self.df.columns.to_list() for col in ext_cols])
    
    @property
    def replicated(self):
        """Return True if the dataset in Master format"""

        rep_cols = ['appseqno', 'final_decision', 'uw58_flag']
        return all([col in self.df.columns.to_list() for col in rep_cols])
    
    @property
    def master_merged(self):
        """Return True if the dataset in Master format and has merged columns"""

        rep_cols = ['appseqno', 'final_decision', 'uw58_flag', 
                    'bcn_merged', 'bni_merged', 'income_merged', 'customscore_merged']
        return all([col in self.df.columns.to_list() for col in rep_cols])
    
    @property
    def keys(self):
        """A dictionary of variable names that maps self-defined keys to the keys in dataset based on its format (EDH, Master, Equifax)"""

        key_1 = ['p_key', 'tier', 'status', 'bk_status', 'bk_all', 'pmt_status', 'cs_seg']
        key_2 = ['uw21_ltv', 'uw48_cbage', 'uw49_ot', 'uw57_pti', 'uw58_tdsr', 'cltage']
        key_3 = ['bcn9', 'bni', 'cscore']
        key_4 = ['ap_amt', 'balance']
        key_5 = ['uw76_income', 'uw20_activetrades', 'uw22_3rtrades', 'uw55_badtrades',
                    'uw8_bib', 'uw192_cald', 'uw34_bir']
        key_6 = ['lightduty_flag', 'uw50_ageot']

        val_1 = ['appseqno', 'mostrecentgrade', 'decisionstatus', 'bookingstatus', None, None, None]
        val_2 = ['uw21_ltv', 'uw48_credburage', 'uw49_opentrades', 'uw57_pti',
                    'uw58_tdsr', 'collatage']
        val_3 = ['uw44_bcn9', 'uw45_bni', 'customscore']
        val_4 = ['requested_amount', None]
        val_5 = ['uw76_grossannualincome', 'uw20_noofactivetrades', 'uw22_noof3plusratedtrades', 'uw55_badtrades_789rated',
                    'uw8_bureauindicatesbankruptcy', 'uw192_currentautoloandelinq', 'uw34_bureauindicatesrepossess']
        val_6 = [None, None]

        if self.external:
            val_1 = ['EFX_CLIENT_INDEX', 'TIER', 'FINAL_DECISION', 'CIBC_BOOKED_LOAN', 'BOOKED_LOAN', 'ACC_STATUS', 'CUSTOM_SCORES_SEG']
            val_2 = ['UW21_ACT', 'UW48_ACT', 'UW49_ACT', 'UW57_ACT',
                        'UW58_ACT', 'COLLATAGE_ACT']
            val_3 = ['UW44_ACT', 'UW45_ACT', 'CUSTOM_SCORES']
            val_4 = ['APPROVED_AMOUNT_NUM', 'BALANCE']
            val_5 = ['UW76_ACT', 'UW20_ACT', 'UW22_ACT', 'UW55_ACT',
                    'UW8_ACT', 'UW192_ACT', 'UW34_ACT']
            val_6 = ['LIGHTDUTY_FLAG', 'UW50_ACT']

        elif self.replicated:
            val_1 = ['appseqno', 'tier', 'final_decision', 'BOOKED', None, 'DLQ', None]
            val_2 = ['uw21_act', 'uw48_act', 'uw49_act', 'uw57_act',
                        'uw58_act', 'collatage_act']
            val_3 = ['uw44_act', 'uw45_act', 'amt_table_customscore']
            val_4 = ['approved_amount_num', 'DWO_BALANCE']
            val_5 = ['uw76_act', 'uw20_act', 'uw22_act', 'uw55_act',
                        'uw8_flag', 'uw192_act', 'uw34_flag']
            val_6 = ['lightdutypoi_flag', 'uw50_act']

            if self.master_merged:
                val_2 = ['ltv_ptiltvtable', 'uw48_act', 'uw49_act', 'pti_ptiltvtable',
                        'tdsr_ptiltvtable', 'collatage_act']
                val_3 = ['bcn_merged', 'bni_merged', 'customscore_merged']
                val_5 = ['income_merged' if val == 'uw76_act' else val for val in val_5]
        
        keys = key_1 + key_2 + key_3 + key_4 + key_5 + key_6
        vals = val_1 + val_2 + val_3 + val_4 + val_5 + val_6

        all_keys = {keys[i]: vals[i] for i in range(len(keys))}

        if self._keys == {}:
            return all_keys
        else:
            return self._keys
    
    @keys.setter
    def keys(self, new_keys):
        """Set the keys property by replacing it with new dictionary of variable names

        :param new_keys: a dictionary of variable names mapping in the same structure of keys property
        """
        self._keys = new_keys


    @property
    def p_key(self):
        """Define the primary of the dataset"""
        return self.keys['p_key']

    @property  
    def vals(self):
        """Dictionary of mapped values of self defined names"""
        key_1 = ['AutoApprove', 'C_Booked', 'ManualApprove_Cl', 'ManualApprove_Cd',
                    'AutoDecline', 'ManualDecline', 'Reapprove']
        
        key_2 = ['Bad_status']
            
        val_1 = ['APPSCOR', (2,3), 'APPROVE', 'APPCOND',
                    'DECSCOR', 'DECLINE', 'REAPPROVE']
        val_2 = [None]

        if self.external:
            val_1 = ['System Approved', (1,), 'Approved', 'Approved with conditions',
                        'System Declined', 'Declined', None]
            
            val_2 = [('DWO', 'NPNA', '31-60 DAYS', '61-90 DAYS', '90+ DAYS')]

        elif self.replicated:
            val_1 = ['APPSCOR', (1,), 'APPROVE', 'APPCOND',
                    'DECSCOR', 'DECLINE', 'REAPPROVE']
        
            val_2 = [('DWO', 'NPNA', '31-60_DLQ', '61-90_DLQ', '91+_DLQ')]

        keys = key_1 + key_2
        vals = val_1 + val_2

        all_vals = {keys[i]: vals[i] for i in range(len(keys))}

        if self._vals == {}:
            return all_vals
        else:
            return self._vals 
    
    @vals.setter
    def vals(self, new_vals):
        """Set the vals property by replacing it with new dictionary of values

        :param new_vals: a dictionary of values mapped in the same structure of vals property
        """
        self._vals = new_vals

    def k(self, dt, key):
        """Create conditions using self.keys"""
        return dt[self.keys[key]]

    ## TTD
    @property
    def dft(self):
        """Dataset: Tier A, B, C"""
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[conda | condb | condc]

    ## Auto Approved
    @property
    def dfa(self):
        """Dataset: Auto-approved"""
        cond = self.k(self.df, 'status') == self.vals['AutoApprove']
        return self.df[cond]

    @property
    def dfta(self):
        """Dataset: Auto-approved Tier A/B/C"""
        cond = self.k(self.df, 'status') == self.vals['AutoApprove']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]
    
    @property
    def dfat(self):
        """Dataset: Auto-approved Tier A/B/C"""
        cond = self.k(self.df, 'status') == self.vals['AutoApprove']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]
    
    ## Manual Approval
    @property
    def dfm(self):
        """Dataset: Manual-approved All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        cond2 = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        return self.df[cond1 | cond2]
    
    @property
    def dfmt(self):
        """Dataset: Manual-approved Tier A/B/C"""
        cond1 = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        cond2 = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[(cond1 | cond2) & (conda | condb | condc)]

    @property
    def dfma(self):
        """Dataset: Manual-approved (clean) All tiers"""
        cond = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        return self.df[cond]

    @property
    def dfmat(self):
        """Dataset: Manual-approved (clean) Tier A/B/C"""
        cond = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]

    @property
    def dfmc(self):
        """Dataset: Manual-approved (with condition) All tiers"""
        cond = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        return self.df[cond]

    @property
    def dfmct(self):
        """Dataset: Manual-approved (with condition) Tier A/B/C"""
        cond = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]

    # Decline
    @property
    def dfd(self):
        """Dataset: All declined All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['AutoDecline']
        cond2 = self.k(self.df, 'status') == self.vals['ManualDecline']
        return self.df[cond1 | cond2]
    
    @property
    def dfdt(self):
        """Dataset: All declined Tier ABC"""
        cond1 = self.k(self.df, 'status') == self.vals['AutoDecline']
        cond2 = self.k(self.df, 'status') == self.vals['ManualDecline']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[(cond1 | cond2) & (conda | condb | condc)]


    @property
    def dfad(self):
        """Dataset: Auto-declined All tiers"""
        cond = self.k(self.df, 'status') == self.vals['AutoDecline']
        return self.df[cond]
    
    @property
    def dfadt(self):
        """Dataset: Auto-declined Tier A B C"""
        cond = self.k(self.df, 'status') == self.vals['AutoDecline']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]
    
    @property
    def dfmd(self):
        """Dataset: Manual-declined All tiers"""
        cond = self.k(self.df, 'status') == self.vals['ManualDecline']
        return self.df[cond]
    
    @property
    def dfmdt(self):
        """Dataset: Manual-declined Tier A B C"""
        cond = self.k(self.df, 'status') == self.vals['ManualDecline']
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]
    
    @property
    def dfd_bk(self):
        '''Declined and booked elsewhere'''
        cond1 = self.k(self.df, 'status') == self.vals['AutoDecline']
        cond2 = self.k(self.df, 'status') == self.vals['ManualDecline']
        condb = self.k(self.df, 'bk_all') == 1
        return self.df[(cond1 | cond2) & condb]

    # Booking
    @property
    def dfbk(self):
        """Dataset: Booked All tiers"""
        cond = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        return self.df[cond]
    
    @property
    def dftbk(self):
        """Dataset: Booked Tier A/B/C"""
        cond = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]

    @property
    def dfbkt(self):
        """Dataset: Booked Tier A/B/C"""
        cond = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond & (conda | condb | condc)]
    
    @property
    def dfaap_bk(self):
        """Dataset: System Approved & Booked All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['AutoApprove']
        cond2 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        return self.df[cond1 & cond2]
    
    @property
    def dfaapt_bk(self):
        """Dataset: System Approved & Booked Tier A B C"""
        cond1 = self.k(self.df, 'status') == self.vals['AutoApprove']
        cond2 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond1 & cond2 & (conda | condb | condc)]
    
    @property
    def dfm_bk(self):
        """Dataset: Manual Approved & Booked All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        cond2 = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        cond3 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        return self.df[(cond1 | cond2) & cond3]
    
    @property
    def dfmt_bk(self):
        """Dataset: Manual Approved & Booked All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        cond2 = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        cond3 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[(cond1 | cond2) & cond3 & (conda | condb | condc)]

    @property
    def dfma_bk(self):
        """Dataset: Manual Approved (Clean) & Booked All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['ManualApprove_Cl']
        cond2 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        return self.df[cond1 & cond2]
    
    @property
    def dfmc_bk(self):
        """Dataset: Manual Approved (Conditional) & Booked All tiers"""
        cond1 = self.k(self.df, 'status') == self.vals['ManualApprove_Cd']
        cond2 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        return self.df[cond1 & cond2]
    

    ## Bad Loans
    @property
    def dfbk_bd(self):
        """Dataset: Booked Bad Loans - All tiers"""
        cond1 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        cond2 = self.k(self.df, 'pmt_status').isin(self.vals['Bad_status'])
        return self.df[cond1 & cond2]
    
    @property
    def dfbkt_bd(self):
        """Dataset: Booked Bad Loans - Tier A B C"""
        cond1 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        cond2 = self.k(self.df, 'pmt_status').isin(self.vals['Bad_status'])
        conda = self.k(self.df, 'tier') == 'A'
        condb = self.k(self.df, 'tier') == 'B'
        condc = self.k(self.df, 'tier') == 'C'
        return self.df[cond1 & cond2 & (conda | condb | condc)]
    
    @property
    def dfaap_bk_bd(self):
        """Dataset: Auto-approved and Booked Bad Loans - All tiers"""
        cond0 = self.k(self.df, 'status') == self.vals['AutoApprove']
        cond1 = self.k(self.df, 'bk_status').isin(self.vals['C_Booked'])
        cond2 = self.k(self.df, 'pmt_status').isin(self.vals['Bad_status'])
        return self.df[cond0 & cond1 & cond2]

    ## Applying Strategy
    # All Incremental
    @property
    def df_incr(self):
        """Dicts of Dataset: incrementals of each strategy TTD"""
        return self.strategy.incr(self.df, self.keys) \
                if self.strategy is not None else None
    
    @property
    def df_incr_ttl(self):
        """Dataset: incremental dataset with all rules (dups removed)"""
        if self.strategy is not None:
            dfs = list(self.df_incr.values())
            return pd.concat(dfs).drop_duplicates()
        
        return None

    # Incremental: Auto Approved

    @property
    def df_incr_aap(self):
        """Dicts of Dataset: incrementals of each strategy that are auto approved"""
        return self.strategy.incr(self.dfa, self.keys) \
                if self.strategy is not None else None
    
    @property
    def df_incr_aapt(self):
        """Dicts of Dataset: incrementals of each strategy that are auto approved"""
        return self.strategy.incr(self.dfat, self.keys) \
                if self.strategy is not None else None
    
    @property
    def df_incr_aap_ttl(self):
        """Dataset: incremental dataset with all rules (dups removed) that are auto approved"""
        if self.strategy is not None:
            dfs = list(self.df_incr_aap.values())
            return pd.concat(dfs).drop_duplicates()

    @property
    def df_incr_aapt_ttl(self):
        """Dataset: incremental dataset with all rules (dups removed) that are auto approved"""
        if self.strategy is not None:
            dfs = list(self.df_incr_aapt.values())
            return pd.concat(dfs).drop_duplicates()
        
        return None
    
    @property
    def df_no_incr_aap_ttl(self):
        """Dataset: dataset without incremental of all rules (dups removed) that are auto approved"""
        if self.strategy is not None:
            ids = self.df_incr_aap_ttl[self.p_key].tolist()
            df = self.df.loc[~self.df[self.p_key].isin(ids)]
            return df
        
        return None
    
    # Delta
    @property
    def df_delta(self):
        """Dicts of Dict of Dataset: Delta of each strategy TTD"""
        return self.strategy.delta(self.df, self.keys) \
                if self.strategy is not None else None


    
    # Violation: TTD
    @property
    def df_vlt(self):
        """Dicts of Dataset: violations of each strategy"""
        return self.strategy.vlt(self.df, self.keys) \
                if self.strategy is not None else None
    
    @property
    def df_vlt_ttl(self):
        """Dataset: violation dataset of any rules (dups removed)"""
        if self.strategy is not None and self.df_vlt is not None:
            dfs = list(self.df_vlt.values())
            return pd.concat(dfs).drop_duplicates()
        
        return None
    
    # Violation: Auto Approved
    @property
    def df_vlt_aapt(self):
        """Dicts of Dataset: violations of each strategy"""
        return self.strategy.vlt(self.dfat, self.keys) \
                if self.strategy is not None else None
    
    @property
    def df_vlt_aapt_ttl(self):
        """Dataset: violation dataset of any rules (dups removed)"""
        if self.strategy is not None and self.df_vlt_aapt is not None:
            dfs = list(self.df_vlt_aapt.values())
            return pd.concat(dfs).drop_duplicates()
        
        return None
    
    # Violation: Declined
    @property
    def df_vlt_d(self):
        """Dicts of Dataset: violations of each strategy"""
        return self.strategy.vlt(self.dfd, self.keys) \
                if self.strategy is not None else None
    
    @property
    def df_vlt_d_ttl(self):
        """Dataset: violation dataset of any rules (dups removed)"""
        if self.strategy is not None and self.df_vlt_d is not None:
            dfs = list(self.df_vlt_d.values())
            return pd.concat(dfs).drop_duplicates()
        
        return None
    



    ## Dates Methods and Attributes(Properties)
    def format_date(self):
        """Add a number of variables to the main dataset that can identify the day/month/year of the application"""
        date_cols = ['Date', 'Date_str', 'Year', 'Year_str', 'Month', 
                        'Month_str', 'Day', 'Day_str']
        if all([col in self.df.columns.to_list() for col in date_cols]):
            pass

        elif self.external:
            self.df['INITIATION_DT'] = self.df['INITIATION_DT'].astype(int)
            self.df['INITIATION_DT'] = self.df['INITIATION_DT'].astype(str)

            self.df['INITIATION_DT'] = self.df['INITIATION_DT'] + '01'
            self.df['Date'] = self.df['INITIATION_DT'].astype(int)
            self.df['Date_str'] = self.df['INITIATION_DT'].astype(str)

            
            self.df['Year_str'] = self.df['Date_str'].str[:4]
            self.df['Year'] = self.df['Year_str'].astype(int)
            self.df['Month_str'] = self.df['Date_str'].str[4:6]
            self.df['Month'] = self.df['Month_str'].astype(int)
            self.df['Day_str'] = self.df['Date_str'].str[6:]
            self.df['Day'] = self.df['Day_str'].astype(int)

        else:
            date_cols = ['initiationdate_year', 'initiationdate_month', 'initiationdate_day']
            for col in date_cols:
                self.df[col] = self.df[col].astype(str)
                self.df.loc[self.df[col].apply(len) == 1, col] = '0' + self.df[col]
            
            self.df['INITIATION_DT'] = self.df['initiationdate_year'] + \
                                        self.df['initiationdate_month'] + \
                                        self.df['initiationdate_day']
            
            self.df['Date'] = self.df['INITIATION_DT'].astype(int)
            self.df['Date_str'] = self.df['INITIATION_DT'].astype(str)

            self.df['Year_str'] = self.df['Date_str'].str[:4]
            self.df['Year'] = self.df['Year_str'].astype(int)
            self.df['Month_str'] = self.df['Date_str'].str[4:6]
            self.df['Month'] = self.df['Month_str'].astype(int)
            self.df['Day_str'] = self.df['Date_str'].str[6:]
            self.df['Day'] = self.df['Day_str'].astype(int)
    
    @property
    def start_date(self):
        """The earliest initiation date of the dataset"""
        self.format_date()
        date = str(self.df['Date'].min())
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        start_date = datetime.datetime(year, month, day)
        return start_date


    @property
    def end_date(self):
        """The latest initiation date of the dataset"""
        self.format_date()
        date = str(self.df['Date'].max())
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        end_date = datetime.datetime(year, month, day)
        return end_date


    def time_frame(self, frame=None, start=None, end=None):
        '''Slice the main dataset based on time period choosen
        
        :frame param: tuple or list of 2 integers in the form of YYYYMMDD (e.g. 20210512)
        :start param: integer in the form of YYYYMMDD (e.g. 20210512), indicating the earliest date (not with frame param)
        :end param: integer in the form of YYYYMMDD (e.g. 20210512), indicating the latest date (not with frame param)
        '''
        self.format_date()

        if frame is not None:
            cond1 = self.df['Date'] >= frame[0]
            cond2 = self.df['Date'] <= frame[1]
            self.df = self.df[cond1 & cond2]
        
        if start is not None:
            cond = self.df['Date'] >= start
            self.df = self.df[cond]
        
        if end is not None:
            cond = self.df['Date'] <= end
            self.df = self.df[cond]

    @functools.cached_property
    def monthly_dfs(self):
        '''Returns the dictionary of monthly datasets of the main dataset'''
        self.format_date()
        df = self.df
        months = self.months

        monthly = {}
        for month in months:
            df_month = df[df['Month'] == month]
            monthly[month] = df_month
            
        return monthly

    @functools.cached_property
    def yearly_dfs(self):
        '''Returns the dictionary of yearly datasets of the main dataset'''
        self.format_date()
        df = self.df

        years = sorted(df['Year'].unique().tolist())
        yearly = {}

        for year in years:
            df_year = df[df['Year'] == year]
            yearly[year] = df_year
        
        return yearly
    
    @property
    def years(self):
        """The years of all records in the main dataset"""
        return sorted(list(self.yearly_dfs.keys()))
    
    @functools.cached_property
    def yearly_monthly_dfs(self):
        yearly = self.yearly_dfs
        months = self.months

        yearly_monthly = {}
        for year, df in yearly.items():
            monthly = {}
            for month in months:
                df_month = df[df['Month'] == month]
                monthly[month] = df_month
            
            yearly_monthly[year] = monthly
        return yearly_monthly

    @functools.cached_property
    def f_yearly_dfs(self):
        """The dictionary of each fiscal year's datasets of the main dataset"""
        f_months = self.f_months
        f_mth_start = f_months[0]
        f_mth_end = f_months[-1]
        
        self.format_date()
        df = self.df

        years = sorted(df['Year'].unique().tolist())
        f_yearly = {}

        for year in years:
            # In Previous Calender Year
            cond_py = df['Year'] == year - 1
            cond_s = df['Month'] >= f_mth_start
            cond1 = cond_py & cond_s

            # In Current Calender Year
            cond_cy = df['Year'] == year
            cond_e = df['Month'] <= f_mth_end
            cond2 = cond_cy & cond_e
            
            df_fyear = df[cond1 | cond2]
            if not df_fyear.empty:
                f_yearly[f'F{year}'] = df_fyear

        # Handle the next coming fiscal year
        cond_ny = df['Year'] == years[-1]
        cond_s = df['Month'] >= f_mth_start
        cond3 = cond_ny & cond_s
        df_fyear_ny = df[cond3]
        if not df_fyear_ny.empty:
            f_yearly[f'F{years[-1] + 1}'] = df_fyear_ny

        return f_yearly
    
    @property
    def f_years(self):
        """The fiscal years of all records in the main dataset"""
        return sorted(list(self.f_yearly_dfs.keys()))
    
    @functools.cached_property
    def f_yearly_monthly_dfs(self):
        """The dictionary of each fiscal year's monthly datasets of the main dataset"""
        f_yearly = self.f_yearly_dfs
        f_months = self.f_months

        f_yearly_monthly = {}
        for f_year, df in f_yearly.items():
            f_monthly = {}
            for f_month in f_months:
                df_f_month = df[df['Month'] == f_month]
                f_monthly[f_month] = df_f_month
            
            f_yearly_monthly[f_year] = f_monthly
        return f_yearly_monthly



    ## Filter Method
    # Convert Flag Names
    def replicate_flags(self, flags):
        for flag in flags.flags:
            this_flag = flag

            if this_flag.composite:
                self.replicate_flags(this_flag)
            else:
                this_flag.name = this_flag.name.lower()

                flag_vals = self.df[this_flag.name].unique().tolist()
                if 'T' in flag_vals or 'F' in flag_vals:
                    if this_flag.val == 1:
                        this_flag.val = 'T'
                    elif this_flag.val == 0:
                        this_flag.val = 'F'


    def apply_filter(self, mode=True):
        if self.filter is not None:

            # Transform Flag Name
            if self.replicated:
                for flag in self.filter.flags:
                    this_flag = flag

                    if this_flag.name not in self.df.columns.tolist():

                        if this_flag.composite:
                            self.replicate_flags(this_flag)
                        else:
                            this_flag.name = this_flag.name.lower()
                            
                            flag_vals = self.df[this_flag.name].unique().tolist()
                            if 'T' in flag_vals or 'F' in flag_vals:
                                if this_flag.val == 1:
                                    this_flag.val = 'T'
                                elif this_flag.val == 0:
                                    this_flag.val = 'F'

            if mode:
                self.df = self.filter.true(self.df)
            else:
                self.df = self.filter.false(self.df)
            


