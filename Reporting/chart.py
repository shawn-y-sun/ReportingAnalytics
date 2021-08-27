from .data import DataFrame, DataSource
import pandas as pd
import datetime
import copy
import math
from .load import load_data
import win32com.client
import functools
from functools import lru_cache
from .helper import move_sheets, hide_tabs
from tqdm import tqdm

class ChartSheet:

    def __init__(self, name, data_source, sheet_name, usecols=None):
        self.name = name
        self.data_source = data_source
        self.sheet_name = sheet_name
        self.usecols = usecols

        self.dfs = []
    
    @functools.cached_property
    def loaded_df(self):
        return load_data(self.data_source.source_file,
                            sheet_name=self.sheet_name,
                            header=None,
                            usecols=self.usecols)
    
    def __add__(self, dataframe):
        self.dfs.append(dataframe)


class ChartFile:

    def __init__(self, chart_file_path):
        self.chart_file_path = chart_file_path

        # Create attributes
        self.chartsheets = []
    
    @functools.cached_property
    def writer(self):
        return pd.ExcelWriter(self.chart_file_path, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
    
    @functools.cached_property
    def workbook(self):
        return self.writer.book
    
    def __add__(self, chartsheet):
        self.chartsheets.append(chartsheet)
    
    @property
    def destination(self):
        return self.chartsheets[0].data_source.file_path
    
    def add_series_helper(self, df, chart, chart_attr, series_attr, data_sheetname,
                            data_start_row, data_start_col):
        col_len = len(df.columns.tolist())
        row_len = len(df.index)
        if chart_attr['type'] == 'column' and chart_attr['subtype'] == 'stacked':
            for row_num in range(data_start_row, data_start_row + row_len):
                series_attr['name'] = [data_sheetname, row_num + 1, data_start_col]
                series_attr['categories'] = [data_sheetname,
                                                data_start_row, data_start_col+1,
                                                data_start_row, data_start_col+1+col_len]
                series_attr['values'] = [data_sheetname,
                                            row_num + 1, data_start_col+1,
                                            row_num + 1, data_start_col+1+col_len]
                chart.add_series(series_attr)

    
    def write(self, startrow=2, startcol=1, gap=2, merge=True, hide=True):
        for chartsheet in tqdm(self.chartsheets, desc='Writing ChartSheets',
                            unit='chart sheet', leave=False):
            data_sheetname = f'{chartsheet.name}_data'
            chart_sheetname = chartsheet.name

            current_datasheet = self.workbook.add_worksheet(data_sheetname)
            current_chartsheet = self.workbook.add_worksheet(chart_sheetname)

            self.writer.sheets[data_sheetname] = current_datasheet
            self.writer.sheets[chart_sheetname] = current_chartsheet

            data_start_row = startrow
            chart_start_row = startrow
            for df in chartsheet.dfs:
                ## Get df_rough
                df.df_rough = chartsheet.loaded_df
                
                ## Write DataSheet
                # write dataframe
                df.df_processed.to_excel(self.writer, 
                                            sheet_name=data_sheetname,
                                            startrow=data_start_row,
                                            startcol=startcol)

                # Write df's name
                title_row = data_start_row - 1
                current_datasheet.write_string(title_row, startcol, df.name)

                ## Write ChartSheet
                # Get chart attributes
                attr = copy.deepcopy(df.chart_attributes)
                add_chart = attr['add_chart']
                add_series = attr['add_series']
                set_y_axis = attr['set_y_axis']
                set_x_axis = attr['set_x_axis']
                set_size = attr['set_size']
                set_title = attr['set_title']

                # Create Chart
                chart = self.workbook.add_chart(add_chart)

                # Create series
                self.add_series_helper(df.df_processed, chart, add_chart, add_series,
                                        data_sheetname=data_sheetname,
                                        data_start_row=data_start_row,
                                        data_start_col=startcol)

                # Set Other Attributes
                chart.set_size(set_size)

                set_title['name'] = df.name
                chart.set_title(set_title)

                chart.set_y_axis(set_y_axis)
                chart.set_x_axis(set_x_axis)

                # Update data_start_row
                df_len = df.df_processed.shape[0] + 1
                data_start_row = data_start_row + df_len + gap

                # Insert Chart
                current_chartsheet.insert_chart(chart_start_row, startcol, chart)
                chart_height = math.ceil(288 * set_size['y_scale'] / 20)
                chart_start_row = chart_start_row + chart_height + gap


        self.workbook.close()

        if merge:
            move_sheets(self.chart_file_path, self.destination)
        
        if hide:
            unhidden = ['Distributions Charts', 'Profiles Dashboard']
            hide_tabs(self.destination, unhidden=unhidden)


### Chart File: New Report_v2
chart_file = r'C:\Users\sunsh\Documents\Daily Approval Report\Report\New Report Charts.xlsx'
cf_new_v2 = ChartFile(chart_file)

# Data Source: New Report v2
file_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report\New Report_strat_v2.xlsx'
ds_new_strat_v2 = DataSource(file_path)


## Chart Sheet: TTD Stacked
sheet_name = 'Distributions'
col_names = ['O3', 'AB3', 'AO3', ('AC3', 'AI3'), 'AP3']

# Col Mapper
def col_mapper(col_name):
    if isinstance(col_name, datetime.datetime):
        return f"{col_name.year}-{col_name.month}"
    else:
        return col_name

# Init ChartSheet: Stacked Column Charts
cs_new_dist_ttd_stacked = ChartSheet('Dist_TTD_stk', ds_new_strat_v2, sheet_name)

# Chart Attributes
color = '#404040'
font_name = 'Calibri (Body)'
chart_attr = {
    'add_chart': {'type': 'column', 'subtype': 'stacked'},
    'add_series': {'gap': 50,
                    'data_labels': {'value': True,
                       'num_format': '0.00%',
                       'font': {'color': color}
                    }},
    'set_y_axis': {'num_format': '0%',
                    'max': 1,
                    'major_unit': 0.2,
                    'num_font': {
                        'color': color
                    }},
    'set_x_axis': {'num_font': {
                        'color': color
                    }},
    'set_size': {'x_scale': 2, 'y_scale':1.5},
    'set_title': {'name': 'TTD Distributions by Tier',
                    'name_font': {
                        'name': font_name,
                        'size': 15,
                        'color': color
                    }}

    }
# Dataframes
index = ('B7', 'B11')
cs_new_dist_ttd_stacked + DataFrame('TTD Distribution by Tier', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B14', 'B24')
cs_new_dist_ttd_stacked + DataFrame('TTD Distribution by BCN (All Tiers)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B27', 'B37')
cs_new_dist_ttd_stacked + DataFrame('TTD Distribution by BCN (Tier A)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B40', 'B50')
cs_new_dist_ttd_stacked + DataFrame('TTD Distribution by BCN (Tier B)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B53', 'B63')
cs_new_dist_ttd_stacked + DataFrame('TTD Distribution by BCN (Tier C)', col_names, index, chart_attr, col_mapper=col_mapper)

cf_new_v2 + cs_new_dist_ttd_stacked

## Chart Sheet: AA Stacked
sheet_name = 'Distributions'
col_names = ['O3', 'AB3', 'AO3', ('AC3', 'AI3'), 'AP3']

# Init ChartSheet: Stacked Column Charts
cs_new_dist_aa_stacked = ChartSheet('Dist_AA_stk', ds_new_strat_v2, sheet_name)

# Dataframes
index = ('B70', 'B74')
cs_new_dist_aa_stacked + DataFrame('Auto Approved Distribution by Tier', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B77', 'B87')
cs_new_dist_aa_stacked + DataFrame('Auto Approved Distribution by BCN (All Tiers)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B90', 'B100')
cs_new_dist_aa_stacked + DataFrame('Auto Approved Distribution by BCN (Tier A)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B103', 'B113')
cs_new_dist_aa_stacked + DataFrame('Auto Approved Distribution by BCN (Tier B)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B116', 'B126')
cs_new_dist_aa_stacked + DataFrame('Auto Approved Distribution by BCN (Tier C)', col_names, index, chart_attr, col_mapper=col_mapper)

cf_new_v2 + cs_new_dist_aa_stacked

## Chart Sheet: MA Stacked
sheet_name = 'Distributions'
col_names = ['O3', 'AB3', 'AO3', ('AC3', 'AI3'), 'AP3']

# Init ChartSheet: Stacked Column Charts
cs_new_dist_ma_stacked = ChartSheet('Dist_MA_stk', ds_new_strat_v2, sheet_name)

# Dataframes
index = ('B133', 'B137')
cs_new_dist_ma_stacked + DataFrame('Manual Approved (All) Distribution by Tier', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B140', 'B150')
cs_new_dist_ma_stacked + DataFrame('Manual Approved (All) Distribution by BCN (All Tiers)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B153', 'B163')
cs_new_dist_ma_stacked + DataFrame('Manual Approved (All) Distribution by BCN (Tier A)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B166', 'B176')
cs_new_dist_ma_stacked + DataFrame('Manual Approved (All) Distribution by BCN (Tier B)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B179', 'B189')
cs_new_dist_ma_stacked + DataFrame('Manual Approved (All) Distribution by BCN (Tier C)', col_names, index, chart_attr, col_mapper=col_mapper)

cf_new_v2 + cs_new_dist_ma_stacked

## Chart Sheet: MACL Stacked
sheet_name = 'Distributions'
col_names = ['O3', 'AB3', 'AO3', ('AC3', 'AI3'), 'AP3']

# Init ChartSheet: Stacked Column Charts
cs_new_dist_macl_stacked = ChartSheet('Dist_MACL_stk', ds_new_strat_v2, sheet_name)

# Dataframes
index = ('B196', 'B200')
cs_new_dist_macl_stacked + DataFrame('Manual Approved (Clean) Distribution by Tier', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B203', 'B213')
cs_new_dist_macl_stacked + DataFrame('Manual Approved (Clean) Distribution by BCN (All Tiers)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B216', 'B226')
cs_new_dist_macl_stacked + DataFrame('Manual Approved (Clean) Distribution by BCN (Tier A)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B229', 'B239')
cs_new_dist_macl_stacked + DataFrame('Manual Approved (Clean) Distribution by BCN (Tier B)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B242', 'B252')
cs_new_dist_macl_stacked + DataFrame('Manual Approved (Clean) Distribution by BCN (Tier C)', col_names, index, chart_attr, col_mapper=col_mapper)

cf_new_v2 + cs_new_dist_macl_stacked

## Chart Sheet: MACD Stacked
sheet_name = 'Distributions'
col_names = ['O3', 'AB3', 'AO3', ('AC3', 'AI3'), 'AP3']

# Init ChartSheet: Stacked Column Charts
cs_new_dist_macd_stacked = ChartSheet('Dist_MACD_stk', ds_new_strat_v2, sheet_name)

# Dataframes
index = ('B259', 'B263')
cs_new_dist_macd_stacked + DataFrame('Manual Approved (Conditional) Distribution by Tier', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B266', 'B276')
cs_new_dist_macd_stacked + DataFrame('Manual Approved (Conditional) Distribution by BCN (All Tiers)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B279', 'B289')
cs_new_dist_macd_stacked + DataFrame('Manual Approved (Conditional) Distribution by BCN (Tier A)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B292', 'B302')
cs_new_dist_macd_stacked + DataFrame('Manual Approved (Conditional) Distribution by BCN (Tier B)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B305', 'B315')
cs_new_dist_macd_stacked + DataFrame('Manual Approved (Conditional) Distribution by BCN (Tier C)', col_names, index, chart_attr, col_mapper=col_mapper)

cf_new_v2 + cs_new_dist_macd_stacked

## Chart Sheet: BK Stacked
sheet_name = 'Distributions'
col_names = ['O3', 'AB3', 'AO3', ('AC3', 'AI3'), 'AP3']

# Init ChartSheet: Stacked Column Charts
cs_new_dist_bk_stacked = ChartSheet('Dist_BK_stk', ds_new_strat_v2, sheet_name)

# Dataframes
index = ('B322', 'B326')
cs_new_dist_bk_stacked + DataFrame('Booking Distribution by Tier', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B329', 'B339')
cs_new_dist_bk_stacked + DataFrame('Booking Distribution by BCN (All Tiers)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B342', 'B352')
cs_new_dist_bk_stacked + DataFrame('Booking Distribution by BCN (Tier A)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B355', 'B365')
cs_new_dist_bk_stacked + DataFrame('Booking Distribution by BCN (Tier B)', col_names, index, chart_attr, col_mapper=col_mapper)

index = ('B368', 'B378')
cs_new_dist_bk_stacked + DataFrame('Booking Distribution by BCN (Tier C)', col_names, index, chart_attr, col_mapper=col_mapper)

cf_new_v2 + cs_new_dist_bk_stacked