import copy

class Rule:
    """An object storing a single rule's strategy"""

    def __init__(self, var, operator, old_threshold, 
                new_threshold, tier=None, test_delta=None):
        """Create a Rule object
        
        :param var: the self-defined variable name (refer to self.keys in Dataset class)
        :param operator: one of ('lt' , 'gt') if less than threshold would trigger the flag,
            then 'lt', otherwise 'gt'
        :param old_threshold: old threshold of the rule
        :param new_threshold: new threshold of the rule
        :param tier: one of 'A', 'B' and 'C'
        :param test_delta: ignore this one
        """
        self.var = var
        self.op = operator
        self.thr_o = old_threshold
        self.thr_n = new_threshold
        self.tier = tier
        self.test_delta = test_delta
    
    @property
    def keys(self):
        """Map custom keys to alias"""
        key1 = ['uw21_ltv', 'uw48_cbage', 'uw49_ot', 'uw57_pti', 'uw58_tdsr', 'cltage']
        key2 = ['uw50_ageot']
        val1 = ['LTV', 'Credit Bureau Age', 'Open Trades', 'PTI', 
                'TDSR', 'Collateral Age']
        val2 = ['Age of Oldest Trade']
        
        keys = key1 + key2
        vals = val1 + val2
        
        return {keys[i]: vals[i] for i in range(len(keys))}
    
    def __str__(self):
        t_str = f" - Tier {self.tier}" if self.tier is not None else ""
        return f"{self.var} - {self.keys[self.var]}{t_str}"
    
    def incr(self, df, keys):
        """Return the incremental dataset of a rule

        :param df: a pandas dataframe
        :param keys: keys of a Dataset
        :return: return the incremental dataset of a rule
        """
        var_key = keys[self.var]
        t_key = keys['tier']
        
        if self.op == 'lt':
            cond1 = (df[var_key] < self.thr_o)
            cond2 = (df[var_key] >= self.thr_n)
        
        elif self.op == 'gt':
            cond1 = (df[var_key] > self.thr_o)
            cond2 = (df[var_key] <= self.thr_n)

        cond3 = True
        if self.tier is not None:
            cond3 = (df[t_key] == self.tier)
        
        return df[cond1 & cond2 & cond3]
    
    def vlt(self, df, keys):
        var_key = keys[self.var]
        t_key = keys['tier']

        if self.op == 'lt':
            cond1 = (df[var_key] < self.thr_n)
        
        elif self.op == 'gt':
            cond1 = (df[var_key] > self.thr_n)

        cond2 = True
        if self.tier is not None:
            cond2 = (df[t_key] == self.tier)
        
        return df[cond1 & cond2]
    
    def delta(self, df, keys):
        var_key = keys[self.var]
        t_key = keys['tier']
        
        delta_dfs = {}
        if self.op == 'lt':
            cond1_in = (df[var_key] <= self.thr_n + self.test_delta)
            cond2_in = (df[var_key] >= self.thr_n)

            cond1_out = (df[var_key] < self.thr_n)
            cond2_out = (df[var_key] >= self.thr_n - self.test_delta)
        
        elif self.op == 'gt':
            cond1_in = (df[var_key] >= self.thr_n - self.test_delta)
            cond2_in = (df[var_key] <= self.thr_n)

            cond1_out = (df[var_key] > self.thr_n)
            cond2_out = (df[var_key] <= self.thr_n + self.test_delta)

        cond3 = True
        if self.tier is not None:
            cond3 = (df[t_key] == self.tier)
        
        delta_dfs['in'] = df[cond1_in & cond2_in & cond3]
        delta_dfs['out'] = df[cond1_out & cond2_out & cond3]
        
        return delta_dfs


class Strategy:
    """An object storing all rules' changes of a strategy"""

    def __init__(self):
        """Create a Strategy object by building an empty list"""
        self.rules = []
    
    def __add__(self, rule):
        self.rules.append(rule)

    def __len__(self):
        return len(self.rules)
    
    def copy(self):
        return copy.deepcopy(self)

    def incr(self, df, keys):
        """Return the incremental datasets of a all rules in a Strategy

        :param df: a pandas dataframe
        :param keys: keys of a Dataset
        :return: return the dictionary of incremental dataset of each rule
        """
        incr_dfs = {}
        for r in self.rules:
            incr_dfs[str(r)] = r.incr(df, keys)
        
        return incr_dfs
    
    def vlt(self, df, keys):
        vlt_dfs = {}
        for r in self.rules:
            vlt_dfs[str(r)] = r.vlt(df, keys)
        
        return vlt_dfs
    
    def delta(self, df, keys):
        """
        keys: keys of a Dataset
        """
        delta_dfs = {}
        for r in self.rules:
            delta_dfs[str(r)] = r.delta(df, keys)
        
        return delta_dfs
    
    def delta_in(self, df, keys):
        """
        keys: keys of a Dataset
        """
        delta_in_dfs = {}
        for r in self.rules:
            delta_in_dfs[str(r)] = r.delta(df, keys)['in']
        
        return delta_in_dfs
    
    def delta_out(self, df, keys):
        """
        keys: keys of a Dataset
        """
        delta_out_dfs = {}
        for r in self.rules:
            delta_out_dfs[str(r)] = r.delta(df, keys)['out']
        
        return delta_out_dfs


## BRUL 3 Rules
#['uw21', 'uw48', 'uw49', 'uw57', 'uw58', 'cltage']
brul3 = Strategy()
brul3 + Rule('uw49_ot', 'lt', 2, 1)
brul3 + Rule('uw58_tdsr', 'gt', 60, 65, 'A')
brul3 + Rule('uw48_cbage', 'lt', 61, 24)
brul3 + Rule('cltage', 'gt', 8, 10)

# For anamoly monitoring purpose
brul3_a = brul3.copy()
brul3_a + Rule('uw58_tdsr', 'gt', 55, 55, 'B')
brul3_a + Rule('uw58_tdsr', 'gt', 55, 55, 'C')

## TDSR A
st_tdsr = Strategy()
st_tdsr + Rule('uw58_tdsr', 'gt', 65, 65, 'A')

## PTI B
st_pti_b = Strategy()
st_pti_b + Rule('uw57_pti', 'gt', 15, 20, 'B')

## PTI (15-23 POI Req)
st_pti_23 = Strategy()
st_pti_23 + Rule('uw57_pti', 'gt', 15, 23)


## New Brul 3 (+ PTI B)
strategy_new_brul3 = brul3.copy()
strategy_new_brul3 + Rule('uw57_pti', 'gt', 15, 20, 'B')

## Brul 3 (for Testing)
st_brul3_test = Strategy()
st_brul3_test + Rule('uw49_ot', 'lt', 2, 1, test_delta = 1)
st_brul3_test + Rule('uw58_tdsr', 'gt', 60, 65, 'A', test_delta = 3)
st_brul3_test + Rule('uw48_cbage', 'lt', 61, 24, test_delta = 5)
st_brul3_test + Rule('cltage', 'gt', 8, 10, test_delta = 1)
st_brul3_test + Rule('uw57_pti', 'gt', 15, 20, 'B', test_delta = 3)
st_brul3_test + Rule('uw50_ageot', 'lt', 24, 24, test_delta = 5)