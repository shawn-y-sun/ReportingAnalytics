from tkinter.filedialog import askopenfilename
import copy
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
from .helper import sl_new_v3

class Entry:
    """An object that stores information of a metrics to be written in a report"""

    def __init__(self, name, sheet, cell, mtype=None, mtier=None, 
                    monthly=False, yearly=False, fiscal=False,
                    distribution=False):
        """Create a Entry object
         
        :param name: name of the Metrics property,
            if it's  a incremental strategy metrics, set to the full name of the strategy
        :param sheet: index (starts from 1) or name of the worksheet to be written
        :param cell: cell reference in Excel (e.g. A1, B13) to be written
        :param mtype: set to metrics name (incr_aapt) if it's a incremnetal strategy metrics
        :param monthly: set True to break down the dataset to monthly
        :param yearly: set True to break down the dataset to yearly
        :param fiscal: set True to follow fiscal calendar
        :param distribution: set True to turn count metrics by tier or scores into proportion of total
        """
        self.name = name
        self.sheet = sheet
        self.cell = cell
        self.mtype = mtype
        self.mtier = mtier
        self.monthly = monthly
        self.yearly = yearly
        self.fiscal = fiscal
        self.distribution = distribution
    
    def copy(self):
        """Create a copy of itself"""
        return copy.deepcopy(self)


class Entries:
    """An object that serves the collection of Entry objects"""

    def __init__(self):
        """Create a Entries object by creating an empty list"""
        self.entries = []
    
    def __add__(self, entry):
        """Add method that can easily append new Entry or Entries"""
        if isinstance(entry, Entry):
            self.entries.append(entry)
        elif isinstance(entry, Entries):
            self.entries.extend(entry.entries)
    
    def __len__(self):
        return len(self.entries)
    
    def set_new_entries(self, **kwargs):
        """Set the parameters of all entries at once
        
        :param kwargs: set of parameters and its new value
        :return: a copy of Entries with the params of each Entry changed
        """
        entries_copy = copy.deepcopy(self.entries)
        for entry in entries_copy:
            for key, val in kwargs.items():
                setattr(entry, key, val)
        
        Entry_copy = copy.deepcopy(self)
        Entry_copy.entries = entries_copy
        return Entry_copy
    
    def move_all(self, sheet_ind=None, col_ind=None, cols=None, rows=None, inplace=False):
        """Change all entry's cell value at once

        :param sheet_ind: new sheet name or index
        :param col_ind: new column index in upper case letter (e.g. 'A', 'AP')
        :param cols: the number of positions to be moved cross (e.g. 1 means move to right by 1 cell)
        :param rows: the number of positions to be moved up or down (e.g. 1 means move to down by 1 cell)
        :param inplace: set True if you want to modify the entries without returning a new Entries object
        :return: (if inplace is false) a copy of Entries with the cell of each Entry changed
        """
        entries_copy = copy.deepcopy(self.entries)
        for entry in entries_copy:
            xy = coordinate_from_string(entry.cell)
            col = xy[0]
            row = xy[1]

            entry.sheet = sheet_ind if sheet_ind is not None else entry.sheet
            col = col_ind if col_ind is not None else col

            col_num = column_index_from_string(col)
            col_num = col_num + cols if cols is not None else col_num
            row = row + rows if rows is not None else row

            col = get_column_letter(col_num)
            entry.cell = col + str(row)
        
        if inplace:
            self.entries = entries_copy
        else:
            Entry_copy = copy.deepcopy(self)
            Entry_copy.entries = entries_copy
            return Entry_copy


class Template:
    """An object stroing the information of a reporting template"""
    
    def __init__(self, entries, file_name=None, report_name=None, date_format=None, slicers=None):
        """Create a template object

        :param entries: an Entries object with all needed Entry objects
        :param file_name: file path of the excel template
        :param report_name: file name when it's saved
        :param date_format: if there is a date entry, then put in the f-string date format
        :param slicers: an Slicers object storing the slicers to be added
        """
        self.entries = entries
        self.file = file_name if file_name is not None else askopenfilename()
        self.name = report_name if report_name is not None else 'Report'
        self.date_format = date_format
        self.slicers = slicers
    

'''
Daily Report
'''

entries_daily = Entries()
entries_daily + Entry('date', 1, 'A2')
entries_daily + Entry('tl_ttd', 1, 'B4')
entries_daily + Entry('tl_aapt', 1, 'B6')
entries_daily + Entry('tl_incr_aap', 1, 'B11')
# Tier
entries_daily + Entry('tr_ttd', 2, 'B2')
entries_daily + Entry('tr_aapt', 2, 'B10')
entries_daily + Entry('tr_incr_aap', 2, 'B23')
# Strat
entries_daily + Entry('uw49_ot - Open Trades', 3, 'B4', mtype='incr_aapt')
entries_daily + Entry('cltage - Collateral Age', 3, 'K4', mtype='incr_aapt')
entries_daily + Entry('uw48_cbage - Credit Bureau Age', 3, 'B12', mtype='incr_aapt')
entries_daily + Entry('uw58_tdsr - TDSR - Tier A', 3, 'K12', mtype='incr_aapt')


file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\Artifact_Cumulative Report_Template.xlsx'
template_daily = Template(entries_daily, file_name, 'Artifact_Cumulative Report', date_format = r'May12-%B%d %Y')


'''
Scores Bands
'''
entries_scores = Entries()
entries_scores + Entry('date', 1, 'B1')
# BCN
entries_scores + Entry('sc_aap', 1, 'D5', mtier='Total')
entries_scores + Entry('sc_aap', 2, 'D5', mtier='A')
entries_scores + Entry('sc_aap', 3, 'D5', mtier='B')
entries_scores + Entry('sc_aap', 4, 'D5', mtier='C')
# BNI
entries_scores + Entry('sc_aap_bni', 1, 'B26', mtier='Total')
entries_scores + Entry('sc_aap_bni', 2, 'B26', mtier='A')
entries_scores + Entry('sc_aap_bni', 3, 'B26', mtier='B')
entries_scores + Entry('sc_aap_bni', 4, 'B26', mtier='C')


file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\Score bands_New Template.xlsx'
template_scores = Template(entries_scores, file_name, 'Scores Bands', date_format = r'June1-%B%d %Y')


'''
New Report_v4
'''
entries_new_v5 = Entries()

sheet_name_1 = 'Count'
# TTD
entries_new_v5 + Entry('tl_ttd', sheet_name_1, 'C4')
entries_new_v5 + Entry('tr_ttd', sheet_name_1, 'C7')
entries_new_v5 + Entry('sc_ttd', sheet_name_1, 'C14', mtier='Total')
entries_new_v5 + Entry('sc_ttd', sheet_name_1, 'C27', mtier='A')
entries_new_v5 + Entry('sc_ttd', sheet_name_1, 'C40', mtier='B')
entries_new_v5 + Entry('sc_ttd', sheet_name_1, 'C53', mtier='C')
entries_new_v5 + Entry('bni_ttd', sheet_name_1, 'C66', mtier='Total')
entries_new_v5 + Entry('bni_ttd', sheet_name_1, 'C78', mtier='A')
entries_new_v5 + Entry('bni_ttd', sheet_name_1, 'C90', mtier='B')
entries_new_v5 + Entry('bni_ttd', sheet_name_1, 'C102', mtier='C')
entries_new_v5 + Entry('cs_ttd', sheet_name_1, 'C114', mtier='Total')
entries_new_v5 + Entry('cs_ttd', sheet_name_1, 'C128', mtier='A')
entries_new_v5 + Entry('cs_ttd', sheet_name_1, 'C142', mtier='B')
entries_new_v5 + Entry('cs_ttd', sheet_name_1, 'C156', mtier='C')

# Auto approved
entries_new_v5 + Entry('tl_aap', sheet_name_1, 'C171')
entries_new_v5 + Entry('tr_aap', sheet_name_1, 'C174')
entries_new_v5 + Entry('sc_aap', sheet_name_1, 'C181', mtier='Total')
entries_new_v5 + Entry('sc_aap', sheet_name_1, 'C194', mtier='A')
entries_new_v5 + Entry('sc_aap', sheet_name_1, 'C207', mtier='B')
entries_new_v5 + Entry('sc_aap', sheet_name_1, 'C220', mtier='C')
entries_new_v5 + Entry('bni_aap', sheet_name_1, 'C233', mtier='Total')
entries_new_v5 + Entry('bni_aap', sheet_name_1, 'C245', mtier='A')
entries_new_v5 + Entry('bni_aap', sheet_name_1, 'C257', mtier='B')
entries_new_v5 + Entry('bni_aap', sheet_name_1, 'C269', mtier='C')
entries_new_v5 + Entry('cs_aap', sheet_name_1, 'C281', mtier='Total')
entries_new_v5 + Entry('cs_aap', sheet_name_1, 'C295', mtier='A')
entries_new_v5 + Entry('cs_aap', sheet_name_1, 'C309', mtier='B')
entries_new_v5 + Entry('cs_aap', sheet_name_1, 'C323', mtier='C')

# Manual approved
entries_new_v5 + Entry('tl_m', sheet_name_1, 'C338')
entries_new_v5 + Entry('tr_m', sheet_name_1, 'C341')
entries_new_v5 + Entry('sc_m', sheet_name_1, 'C348', mtier='Total')
entries_new_v5 + Entry('sc_m', sheet_name_1, 'C361', mtier='A')
entries_new_v5 + Entry('sc_m', sheet_name_1, 'C374', mtier='B')
entries_new_v5 + Entry('sc_m', sheet_name_1, 'C387', mtier='C')
entries_new_v5 + Entry('bni_m', sheet_name_1, 'C400', mtier='Total')
entries_new_v5 + Entry('bni_m', sheet_name_1, 'C412', mtier='A')
entries_new_v5 + Entry('bni_m', sheet_name_1, 'C424', mtier='B')
entries_new_v5 + Entry('bni_m', sheet_name_1, 'C436', mtier='C')
entries_new_v5 + Entry('cs_m', sheet_name_1, 'C448', mtier='Total')
entries_new_v5 + Entry('cs_m', sheet_name_1, 'C462', mtier='A')
entries_new_v5 + Entry('cs_m', sheet_name_1, 'C476', mtier='B')
entries_new_v5 + Entry('cs_m', sheet_name_1, 'C490', mtier='C')

# Manaual approved (clean)
entries_new_v5 + Entry('tl_ma', sheet_name_1, 'C505')
entries_new_v5 + Entry('tr_ma', sheet_name_1, 'C508')
entries_new_v5 + Entry('sc_ma', sheet_name_1, 'C515', mtier='Total')
entries_new_v5 + Entry('sc_ma', sheet_name_1, 'C528', mtier='A')
entries_new_v5 + Entry('sc_ma', sheet_name_1, 'C541', mtier='B')
entries_new_v5 + Entry('sc_ma', sheet_name_1, 'C554', mtier='C')
entries_new_v5 + Entry('bni_ma', sheet_name_1, 'C567', mtier='Total')
entries_new_v5 + Entry('bni_ma', sheet_name_1, 'C579', mtier='A')
entries_new_v5 + Entry('bni_ma', sheet_name_1, 'C591', mtier='B')
entries_new_v5 + Entry('bni_ma', sheet_name_1, 'C603', mtier='C')
entries_new_v5 + Entry('cs_ma', sheet_name_1, 'C615', mtier='Total')
entries_new_v5 + Entry('cs_ma', sheet_name_1, 'C629', mtier='A')
entries_new_v5 + Entry('cs_ma', sheet_name_1, 'C643', mtier='B')
entries_new_v5 + Entry('cs_ma', sheet_name_1, 'C657', mtier='C')

# Manual approved (conditional)
entries_new_v5 + Entry('tl_mc', sheet_name_1, 'C672')
entries_new_v5 + Entry('tr_mc', sheet_name_1, 'C675')
entries_new_v5 + Entry('sc_mc', sheet_name_1, 'C682', mtier='Total')
entries_new_v5 + Entry('sc_mc', sheet_name_1, 'C695', mtier='A')
entries_new_v5 + Entry('sc_mc', sheet_name_1, 'C708', mtier='B')
entries_new_v5 + Entry('sc_mc', sheet_name_1, 'C721', mtier='C')
entries_new_v5 + Entry('bni_mc', sheet_name_1, 'C734', mtier='Total')
entries_new_v5 + Entry('bni_mc', sheet_name_1, 'C746', mtier='A')
entries_new_v5 + Entry('bni_mc', sheet_name_1, 'C758', mtier='B')
entries_new_v5 + Entry('bni_mc', sheet_name_1, 'C770', mtier='C')
entries_new_v5 + Entry('cs_mc', sheet_name_1, 'C782', mtier='Total')
entries_new_v5 + Entry('cs_mc', sheet_name_1, 'C796', mtier='A')
entries_new_v5 + Entry('cs_mc', sheet_name_1, 'C810', mtier='B')
entries_new_v5 + Entry('cs_mc', sheet_name_1, 'C824', mtier='C')

# Bookings
entries_new_v5 + Entry('tl_bk', sheet_name_1, 'C839')
entries_new_v5 + Entry('tr_bk', sheet_name_1, 'C842')
entries_new_v5 + Entry('sc_bk', sheet_name_1, 'C849', mtier='Total')
entries_new_v5 + Entry('sc_bk', sheet_name_1, 'C862', mtier='A')
entries_new_v5 + Entry('sc_bk', sheet_name_1, 'C875', mtier='B')
entries_new_v5 + Entry('sc_bk', sheet_name_1, 'C888', mtier='C')
entries_new_v5 + Entry('bni_bk', sheet_name_1, 'C901', mtier='Total')
entries_new_v5 + Entry('bni_bk', sheet_name_1, 'C913', mtier='A')
entries_new_v5 + Entry('bni_bk', sheet_name_1, 'C925', mtier='B')
entries_new_v5 + Entry('bni_bk', sheet_name_1, 'C937', mtier='C')
entries_new_v5 + Entry('cs_bk', sheet_name_1, 'C949', mtier='Total')
entries_new_v5 + Entry('cs_bk', sheet_name_1, 'C963', mtier='A')
entries_new_v5 + Entry('cs_bk', sheet_name_1, 'C977', mtier='B')
entries_new_v5 + Entry('cs_bk', sheet_name_1, 'C991', mtier='C')

# AA & Bookings
entries_new_v5 + Entry('tl_aap_bk', sheet_name_1, 'C1006')
entries_new_v5 + Entry('tr_aap_bk', sheet_name_1, 'C1009')
entries_new_v5 + Entry('sc_aap_bk', sheet_name_1, 'C1016', mtier='Total')
entries_new_v5 + Entry('sc_aap_bk', sheet_name_1, 'C1029', mtier='A')
entries_new_v5 + Entry('sc_aap_bk', sheet_name_1, 'C1042', mtier='B')
entries_new_v5 + Entry('sc_aap_bk', sheet_name_1, 'C1055', mtier='C')
entries_new_v5 + Entry('bni_aap_bk', sheet_name_1, 'C1068', mtier='Total')
entries_new_v5 + Entry('bni_aap_bk', sheet_name_1, 'C1080', mtier='A')
entries_new_v5 + Entry('bni_aap_bk', sheet_name_1, 'C1092', mtier='B')
entries_new_v5 + Entry('bni_aap_bk', sheet_name_1, 'C1104', mtier='C')
entries_new_v5 + Entry('cs_aap_bk', sheet_name_1, 'C1116', mtier='Total')
entries_new_v5 + Entry('cs_aap_bk', sheet_name_1, 'C1130', mtier='A')
entries_new_v5 + Entry('cs_aap_bk', sheet_name_1, 'C1144', mtier='B')
entries_new_v5 + Entry('cs_aap_bk', sheet_name_1, 'C1158', mtier='C')

# M & Bookings
entries_new_v5 + Entry('tl_m_bk', sheet_name_1, 'C1173')
entries_new_v5 + Entry('tr_m_bk', sheet_name_1, 'C1176')
entries_new_v5 + Entry('sc_m_bk', sheet_name_1, 'C1183', mtier='Total')
entries_new_v5 + Entry('sc_m_bk', sheet_name_1, 'C1196', mtier='A')
entries_new_v5 + Entry('sc_m_bk', sheet_name_1, 'C1209', mtier='B')
entries_new_v5 + Entry('sc_m_bk', sheet_name_1, 'C1222', mtier='C')
entries_new_v5 + Entry('bni_m_bk', sheet_name_1, 'C1235', mtier='Total')
entries_new_v5 + Entry('bni_m_bk', sheet_name_1, 'C1247', mtier='A')
entries_new_v5 + Entry('bni_m_bk', sheet_name_1, 'C1259', mtier='B')
entries_new_v5 + Entry('bni_m_bk', sheet_name_1, 'C1271', mtier='C')
entries_new_v5 + Entry('cs_m_bk', sheet_name_1, 'C1283', mtier='Total')
entries_new_v5 + Entry('cs_m_bk', sheet_name_1, 'C1297', mtier='A')
entries_new_v5 + Entry('cs_m_bk', sheet_name_1, 'C1311', mtier='B')
entries_new_v5 + Entry('cs_m_bk', sheet_name_1, 'C1325', mtier='C')


## Profiles
sheet_name_profile = 'Profiles'
# TTD
entries_new_v5 + Entry('tr_ttdt', sheet_name_profile, 'C5')
entries_new_v5 + Entry('tr_ttdt_pf', sheet_name_profile, 'C12')

entries_new_v5 + Entry('tr_aapt', sheet_name_profile, 'C80')
entries_new_v5 + Entry('tr_aapt_pf', sheet_name_profile, 'C87')

entries_new_v5 + Entry('tr_mt', sheet_name_profile, 'C155')
entries_new_v5 + Entry('tr_mt_pf', sheet_name_profile, 'C162')

entries_new_v5 + Entry('tr_mat', sheet_name_profile, 'C230')
entries_new_v5 + Entry('tr_mat_pf', sheet_name_profile, 'C237')

entries_new_v5 + Entry('tr_mct', sheet_name_profile, 'C305')
entries_new_v5 + Entry('tr_mct_pf', sheet_name_profile, 'C312')

entries_new_v5 + Entry('tr_bkt', sheet_name_profile, 'C380')
entries_new_v5 + Entry('tr_bkt_pf', sheet_name_profile, 'C387')

entries_new_v5 + Entry('tr_aapt_bk', sheet_name_profile, 'C455')
entries_new_v5 + Entry('tr_aapt_bk_pf', sheet_name_profile, 'C462')

entries_new_v5 + Entry('tr_mt_bk', sheet_name_profile, 'C530')
entries_new_v5 + Entry('tr_mt_bk_pf', sheet_name_profile, 'C537')

entries_new_v5 + Entry('tr_adt', sheet_name_profile, 'C605')
entries_new_v5 + Entry('tr_adt_pf', sheet_name_profile, 'C612')

entries_new_v5 + Entry('tr_mdt', sheet_name_profile, 'C680')
entries_new_v5 + Entry('tr_mdt_pf', sheet_name_profile, 'C687')

entries_new_v5_fy = entries_new_v5.set_new_entries(monthly=True, yearly=True, fiscal=True)
file_name = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\New Report_empty_v5.xlsx'
template_new_v5 = Template(entries_new_v5_fy, file_name, 'New Report_v5')


'''
New Report Updatet_v5
'''
entries_new_update_v5 = entries_new_v5.move_all(col_ind = 'AP')

file_name_v5 = r'C:\Users\sunsh\Documents\Daily Approval Report\Template\New Report Template_v5.xlsx'
template_new_fy_update_v5 = Template(entries_new_update_v5, file_name_v5, 'New Report_Update_v5', slicers=sl_new_v3)
