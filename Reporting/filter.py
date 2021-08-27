import copy

class Flag:

    def __init__(self, name=None, val=1, opt='==', composite=False, logic=None, opposite=False):
        self.name = None if composite else name
        self.val = None if composite else val
        self.opt = None if composite else opt
        self.composite = composite
        self.logic = logic
        self.opposite = opposite
        self.flags = [] if composite else None
    
    def __add__(self, flag):
        self.flags.append(flag)
        
    def __len__(self):
        return len(self.flags)

    def copy(self):
        return copy.deepcopy(self)
    
    def remove(self, inplace=False, **kwargs):
        def detetrmine_remove(flag):
            match = True
            for key, val in kwargs.items():
                if getattr(flag, key) == val:
                    match = match and True
                else:
                    match = match and False
            return match

        if self.composite:
            if inplace:
                self.flags = [flag for flag in self.flags if not detetrmine_remove(flag)]
            else:
                flag_copy = self.copy()
                flag_copy.flags = [flag for flag in self.flags if not detetrmine_remove(flag)]
                return flag_copy

    @property
    def query(self):
        if not self.composite:
            if isinstance(self.val, str):
                query = f"(`{self.name}` {self.opt} '{self.val}')"
            else:
                query = f"(`{self.name}` {self.opt} {self.val})"
        
        else:
            query_list = [flag.query for flag in self.flags]
            query_comp = ' & '.join(query_list) if self.logic == 'and' else ' | '.join(query_list)
            query = '(' + query_comp + ')'

        return query if not self.opposite else f"(~ {query})"
    

class Filter(Flag):

    def __init__(self, logic='or', opposite=False):
        super().__init__(composite=True, logic=logic, opposite=opposite)


    def true(self, df):
        return df.query(self.query, engine='python')
    
    def false(self, df):
        false_query = f"~ {self.query}"
        return df.query(false_query, engine='python')

    def update(self, names, flags):
        filter_copy = copy.deepcopy(self)

        if isinstance(names, str):
            names = [names,]
            flags = [flags,]

        for flag_ind, flag in enumerate(self.flags):
            if flag.name in names:
                new_index = names.index(flag.name)
                filter_copy.flags[flag_ind] = flags[new_index]

        return filter_copy


## Filter: Test
filter_test = Filter('and')
tier_flag = Flag(composite=True, logic='or')
tier_flag + Flag('mostrecentgrade', 'A')
tier_flag + Flag('mostrecentgrade', 'C')
filter_test + tier_flag

date_flag = Flag(composite=True, logic='or')
date_flag + Flag('initiationdate_day', 27)
date_flag + Flag('initiationdate_day', 26)
filter_test + date_flag

## Filter: System Approve
filter_sys_aap = Filter('or')
filter_sys_aap + Flag('DIVESTITURE_FLAG')
filter_sys_aap + Flag('UW47_FLAG')
filter_sys_aap + Flag('COMMERCIALVEHICL_FLAG')
filter_sys_aap + Flag('UW43_FLAG')
filter_sys_aap + Flag('UW62_FLAG')
filter_sys_aap + Flag('UW40_FLAG')
filter_sys_aap + Flag('UW79_FLAG')
filter_sys_aap + Flag('UW74_FLAG')
filter_sys_aap + Flag('UW68_FLAG')
filter_sys_aap + Flag('LIGHTDUTY_FLAG')
filter_sys_aap + Flag('UW45_FLAG')
filter_sys_aap + Flag('UW63_FLAG')
filter_sys_aap + Flag('CIBCERROR_FLAG')
filter_sys_aap + Flag('UW8_FLAG')
filter_sys_aap + Flag('UW26_FLAG')
filter_sys_aap + Flag('UW33_FLAG')
filter_sys_aap + Flag('UW72_FLAG')
filter_sys_aap + Flag('UW9_FLAG')
filter_sys_aap + Flag('UW2_FLAG')
filter_sys_aap + Flag('UW16_FLAG')
filter_sys_aap + Flag('BCN_AUTO_DEC_FLAG')
filter_sys_aap + Flag('UW190_FLAG')
filter_sys_aap + Flag('UW27_FLAG')
filter_sys_aap + Flag('HIGHPTI_FLAG')
filter_sys_aap + Flag('UW28_FLAG')
filter_sys_aap + Flag('UW29_FLAG')
filter_sys_aap + Flag('UW85_FLAG')
filter_sys_aap + Flag('UW86_FLAG')
filter_sys_aap + Flag('UW80_FLAG')
filter_sys_aap + Flag('UW83_FLAG')
filter_sys_aap + Flag('UW82_FLAG')
filter_sys_aap + Flag('FTIERNOTNEWCOMER_FLAG')
filter_sys_aap + Flag('AGEINCOME_FLAG')
filter_sys_aap + Flag('UW50_FLAG')
filter_sys_aap + Flag('CRISTATCODEERR_FLAG')
filter_sys_aap + Flag('LOWTOTALINCOME_FLAG')
filter_sys_aap + Flag('CB7_FLAG')
filter_sys_aap + Flag('AUTOAPPROVETIERC_FLAG')
filter_sys_aap + Flag('UW71_FLAG')
filter_sys_aap + Flag('UW6_FLAG')
filter_sys_aap + Flag('UW58_FLAG') # Brul3
filter_sys_aap + Flag('UW21_FLAG')
filter_sys_aap + Flag('COLLATAGE_FLAG') # Brul3
filter_sys_aap + Flag('UW49_FLAG') # Brul3
filter_sys_aap + Flag('UW48_FLAG') # Brul3

## Filter: Brul 3 Updates
# UW58_FLAG_NEW
UW58_FLAG_NEW = Flag(composite=True, logic='and')
UW58_FLAG_NEW + Flag('UW58_ACT', 70, '>')
UW58_FLAG_NEW + Flag('TIER', 'A', '==')

# COLLATAGE_FLAG_NEW
COLLATAGE_FLAG_NEW = Flag('COLLATAGE_ACT', 10, '>')

# UW49_FLAG_NEW
UW49_FLAG_NEW = Flag('UW49_ACT', 1, '<')

# UW48_FLAG_NEW
UW48_FLAG_NEW = Flag('UW48_ACT', 24, '<')

# LOAN_AMT_FLAG (Add)
LOAN_AMT_FLAG = Flag(composite=True, logic='or')

LOAN_AMT_FLAG_A = Flag(composite=True, logic='and')
LOAN_AMT_FLAG_A + Flag('LOAN_AMOUNT', 100000, '>')
LOAN_AMT_FLAG_A + Flag('TIER', 'A', '==')
LOAN_AMT_FLAG + LOAN_AMT_FLAG_A

LOAN_AMT_FLAG_B = Flag(composite=True, logic='and')
LOAN_AMT_FLAG_B + Flag('LOAN_AMOUNT', 100000, '>')
LOAN_AMT_FLAG_B + Flag('TIER', 'B', '==')
LOAN_AMT_FLAG + LOAN_AMT_FLAG_B

LOAN_AMT_FLAG_C = Flag(composite=True, logic='and')
LOAN_AMT_FLAG_C + Flag('LOAN_AMOUNT', 50000, '>')
LOAN_AMT_FLAG_C + Flag('TIER', 'C', '==')
LOAN_AMT_FLAG + LOAN_AMT_FLAG_C

# Update all
names = ['UW58_FLAG', 'COLLATAGE_FLAG', 'UW49_FLAG', 'UW48_FLAG']
flags = [UW58_FLAG_NEW, COLLATAGE_FLAG_NEW, UW49_FLAG_NEW, UW48_FLAG_NEW]
filter_sys_aap_brul3 = filter_sys_aap.update(names, flags)
filter_sys_aap_brul3 + LOAN_AMT_FLAG

## brul3 Filters with UW21
filters_brul3_w_uw21 = Filter('and')
filters_brul3 = Filter('or')

# UW48
uw48 = Flag(composite=True, logic='or')

uw48_A = Flag(composite=True, logic='and')
uw48_A + Flag('TIER', 'A')
uw48_A + Flag('UW48_ACT', 24, '>=')
uw48_A + Flag('UW48_ACT', 61, '<')
uw48_A + Flag('UW58_ACT', 65, '<=')
uw48 + uw48_A

uw48_B = Flag(composite=True, logic='and')
uw48_B + Flag('TIER', 'B')
uw48_B + Flag('UW48_ACT', 24, '>=')
uw48_B + Flag('UW48_ACT', 61, '<')
uw48_B + Flag('UW58_ACT', 55, '<=')
uw48 + uw48_B

uw48_C = Flag(composite=True, logic='and')
uw48_C + Flag('TIER', 'C')
uw48_C + Flag('UW48_ACT', 24, '>=')
uw48_C + Flag('UW48_ACT', 61, '<')
uw48_C + Flag('UW58_ACT', 55, '<=')
uw48_C + Flag('LOAN_AMOUNT', 50000, '<=')
uw48_C + Flag('UW21_ACT', 120, '<=')
uw48 + uw48_C

filters_brul3 + uw48

# UW49
uw49 = Flag(composite=True, logic='or')

uw49_A = Flag(composite=True, logic='and')
uw49_A + Flag('TIER', 'A')
uw49_A + Flag('UW49_ACT', 1)
uw49_A + Flag('UW58_ACT', 65, '<=')
uw49 + uw49_A

uw49_B = Flag(composite=True, logic='and')
uw49_B + Flag('TIER', 'B')
uw49_B + Flag('UW49_ACT', 1)
uw49_B + Flag('UW58_ACT', 55, '<=')
uw49 + uw49_B

uw49_C = Flag(composite=True, logic='and')
uw49_C + Flag('TIER', 'C')
uw49_C + Flag('UW49_ACT', 1)
uw49_C + Flag('UW58_ACT', 55, '<=')
uw49_C + Flag('LOAN_AMOUNT', 50000, '<=')
uw49_C + Flag('UW21_ACT', 120, '<=')
uw49 + uw49_C

filters_brul3 + uw49

# CollatAge
COLLATAGE = Flag(composite=True, logic='or')

COLLATAGE_A = Flag(composite=True, logic='and')
COLLATAGE_A + Flag('TIER', 'A')
COLLATAGE_A + Flag('COLLATAGE_ACT', 8, '>')
COLLATAGE_A + Flag('COLLATAGE_ACT', 10, '<=')
COLLATAGE_A + Flag('UW58_ACT', 65, '<=')
COLLATAGE + COLLATAGE_A

COLLATAGE_B = Flag(composite=True, logic='and')
COLLATAGE_B + Flag('TIER', 'B')
COLLATAGE_B + Flag('COLLATAGE_ACT', 8, '>')
COLLATAGE_B + Flag('COLLATAGE_ACT', 10, '<=')
COLLATAGE_B + Flag('UW58_ACT', 55, '<=')
COLLATAGE + COLLATAGE_B

COLLATAGE_C = Flag(composite=True, logic='and')
COLLATAGE_C + Flag('TIER', 'C')
COLLATAGE_C + Flag('COLLATAGE_ACT', 8, '>')
COLLATAGE_C + Flag('COLLATAGE_ACT', 10, '<=')
COLLATAGE_C + Flag('UW58_ACT', 55, '<=')
COLLATAGE_C + Flag('LOAN_AMOUNT', 50000, '<=')
COLLATAGE_C + Flag('UW21_ACT', 120, '<=')
COLLATAGE + COLLATAGE_C

filters_brul3 + COLLATAGE

# UW58 - A
uw58 = Flag(composite=True, logic='and')
uw58 + Flag('TIER', 'A')
uw58 + Flag('UW58_ACT', 60, '>')
uw58 + Flag('UW58_ACT', 65, '<=')

filters_brul3 + uw58

# Support filter
uw21 = Flag('UW21_ACT', 0, '>=')

filters_brul3_w_uw21 + filters_brul3
filters_brul3_w_uw21 + uw21



### TDSR A Simulation
filter_tdsr_sim = Filter('and')

## Only TDSR A
tdsr_a = Flag(composite=True, logic='and')
tdsr_a + Flag('TIER', 'A')
tdsr_a + Flag('UW58_ACT', 65, '>')
filter_tdsr_sim + tdsr_a

## New Flag
# COLLATAGE_FLAG_NEW
COLLATAGE_FLAG_NEW = Flag('COLLATAGE_ACT', 10, '>')

# UW49_FLAG_NEW
UW49_FLAG_NEW = Flag('UW49_ACT', 1, '<')

# UW48_FLAG_NEW
UW48_FLAG_NEW = Flag('UW48_ACT', 24, '<')

# LOAN_AMT_FLAG (Add)
LOAN_AMT_FLAG = Flag(composite=True, logic='or')

LOAN_AMT_FLAG_A = Flag(composite=True, logic='and')
LOAN_AMT_FLAG_A + Flag('LOAN_AMOUNT', 100000, '>')
LOAN_AMT_FLAG_A + Flag('TIER', 'A', '==')
LOAN_AMT_FLAG + LOAN_AMT_FLAG_A

LOAN_AMT_FLAG_B = Flag(composite=True, logic='and')
LOAN_AMT_FLAG_B + Flag('LOAN_AMOUNT', 100000, '>')
LOAN_AMT_FLAG_B + Flag('TIER', 'B', '==')
LOAN_AMT_FLAG + LOAN_AMT_FLAG_B

LOAN_AMT_FLAG_C = Flag(composite=True, logic='and')
LOAN_AMT_FLAG_C + Flag('LOAN_AMOUNT', 50000, '>')
LOAN_AMT_FLAG_C + Flag('TIER', 'C', '==')
LOAN_AMT_FLAG + LOAN_AMT_FLAG_C

# Update all
names = ['COLLATAGE_FLAG', 'UW49_FLAG', 'UW48_FLAG']
flags = [COLLATAGE_FLAG_NEW, UW49_FLAG_NEW, UW48_FLAG_NEW]
filter_sys_aap_trsr = filter_sys_aap.update(names, flags)
filter_sys_aap_trsr + LOAN_AMT_FLAG #Sys app filter with TDSR

# Sys app filter without TDSR
filter_sys_aap_no_tdsr = filter_sys_aap_trsr.remove(name='UW58_FLAG') # Remove TDSR flag

filter_tdsr_sim_notblocked = filter_tdsr_sim.copy()

filter_tdsr_sim + filter_sys_aap_no_tdsr



### Bad Rates with TDSR
filter_bad_tdsr = Filter('and')


## Tier
filter_bad_tdsr + Flag('TIER', 'A')

## Sys Apps 
filter_bad_no_tdsr = filter_bad_tdsr.copy()

filter_sys_aap_trsr_op = filter_sys_aap_trsr.copy()
filter_sys_aap_trsr_op.opposite = True
filter_bad_tdsr + filter_sys_aap_trsr_op #with UW58 Flag

filter_sys_aap_no_tdsr_op = filter_sys_aap_no_tdsr.copy()
filter_sys_aap_no_tdsr_op.opposite = True
filter_bad_no_tdsr + filter_sys_aap_no_tdsr_op # without UW58 Flag

filter_tdsr_sim_notblocked + filter_sys_aap_no_tdsr_op

## LightDuty Flag
filter_lightduty = Filter('and')
filter_lightduty + Flag('lightdutypoi_flag', 'T', '==')


##  New BRUL3 Before (w/ PTI)
filter_new_brul3_before = Filter('or')
filter_new_brul3_before + Flag('uw49_act', 2, '<') # UW49

uw58_flag_before = Flag(composite=True, logic='and') #UW58
uw58_flag_before + Flag('uw58_act', 60, '>')
uw58_flag_before + Flag('tier', 'A', '==')
filter_new_brul3_before + uw58_flag_before

filter_new_brul3_before + Flag('uw48_act', 61, '<') # UW48
filter_new_brul3_before + Flag('collatage_act', 8, '>') # collatage

filter_new_brul3_before_nopti = filter_new_brul3_before.copy()

uw57_flag_before = Flag(composite=True, logic='and') #UW57
uw57_flag_before + Flag('uw57_act', 15, '>')
uw57_flag_before + Flag('tier', 'B', '==')
filter_new_brul3_before + uw57_flag_before


##  New BRUL3 After (w/ PTI)
filter_new_brul3_after = Filter('or')
filter_new_brul3_after + Flag('uw49_act', 1, '<') # UW49

uw58_flag_after = Flag(composite=True, logic='and') #UW58
uw58_flag_after + Flag('uw58_act', 65, '>')
uw58_flag_after + Flag('tier', 'A', '==')
filter_new_brul3_after + uw58_flag_after

filter_new_brul3_after + Flag('uw48_act', 24, '<') # UW48
filter_new_brul3_after + Flag('collatage_act', 10, '>') # collatage

filter_new_brul3_after_nopti = filter_new_brul3_after.copy()

uw57_flag_after = Flag(composite=True, logic='and') #UW57
uw57_flag_after + Flag('uw57_act', 20, '>')
uw57_flag_after + Flag('tier', 'B', '==')
filter_new_brul3_after + uw57_flag_after