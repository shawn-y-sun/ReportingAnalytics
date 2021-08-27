import pandas as pd
import datetime
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
import win32com.client
import functools


class DataFrame:

    def __init__(self, name, col_cells=None, index_cells=None,
                    chart_attributes=None,col_mapper=None):
        self.name = name
        self.col_cells = col_cells
        self.index_cells = index_cells
        self.chart_attributes = chart_attributes
        self.col_mapper = col_mapper

        # Create attributes
        self.df_rough = None


    def expand_cols(self, _range):
        cell_1 = _range[0]
        cell_2 = _range[1]

        col_cells = [cell_1,]
        while col_cells[-1] != cell_2:
            xy = coordinate_from_string(cell_1)
            col = xy[0]
            row = xy[1]     

            col_ind = column_index_from_string(col)
            new_col_ind = col_ind + 1
            new_col = get_column_letter(new_col_ind)
            new_cell = new_col + str(row)
            col_cells.append(new_cell)
            cell_1 = new_cell

        return col_cells
    
    def expand_rows(self, _range):
        cell_1 = _range[0]
        cell_2 = _range[1]

        row_cells = [cell_1,]
        while row_cells[-1] != cell_2:
            xy = coordinate_from_string(cell_1)
            col = xy[0]
            row = xy[1]     

            new_row = row + 1
            new_cell = col + str(new_row)
            row_cells.append(new_cell)
            cell_1 = new_cell

        return row_cells


    @property
    def flatten_colcells(self):
        flatten_colcells = []

        if isinstance(self.col_cells, list):
            for col in self.col_cells:
                if isinstance(col, str):
                    flatten_colcells.append(col)
                elif isinstance(col, tuple):
                    expanded_range = self.expand_cols(col)
                    flatten_colcells.extend(expanded_range)

        elif isinstance(self.col_cells, tuple):
            flatten_colcells = self.expand_cols(self.col_cells)
        
        elif isinstance(self.col_cells, str):
            flatten_colcells.append(self.col_cells)

        return flatten_colcells
    
    @property
    def flatten_indexcells(self):
        flatten_indexcells = []

        if isinstance(self.index_cells, list):
            for index in self.index_cells:
                if isinstance(index, str):
                    flatten_indexcells.append(index)
                elif isinstance(index, tuple):
                    expanded_range = self.expand_rows(index)
                    flatten_indexcells.extend(expanded_range)

        elif isinstance(self.index_cells, tuple):
            flatten_indexcells = self.expand_rows(self.index_cells)
        
        elif isinstance(self.index_cells, str):
            flatten_indexcells.append(self.index_cells)

        return flatten_indexcells
    
    
    def get_val(self, cell):
        xy = coordinate_from_string(cell)
        col = xy[0]
        col_ind = column_index_from_string(col)
        row = xy[1] 

        df_row = row - 1
        df_col = col_ind -1

        return self.df_rough.iloc[df_row, df_col]
    
    def get_ind(self, cell):
        xy = coordinate_from_string(cell)
        col = xy[0]
        col_ind = column_index_from_string(col) - 1
        row = xy[1] - 1

        return (row, col_ind)


    @property
    def flatten_colnames(self):
        flatten_colnames = [self.get_val(x) for x in self.flatten_colcells]
        if self.col_mapper is not None:
            flatten_colnames = [x for x in map(self.col_mapper, flatten_colnames)]
        return flatten_colnames
    
    @property
    def flatten_indexnames(self):
        flatten_indexnames = [self.get_val(x) for x in self.flatten_indexcells]
        return flatten_indexnames
    
    @property
    def flatten_colind(self):
        flatten_colind = [self.get_ind(x)[1] for x in self.flatten_colcells]
        return flatten_colind
    
    @property
    def flatten_indexind(self):
        flatten_indexind = [self.get_ind(x)[0] for x in self.flatten_indexcells]
        return flatten_indexind
        
    
    @property
    def df_processed(self):
        df = self.df_rough
        
        df = df.iloc[self.flatten_indexind, self.flatten_colind]
        df.columns = self.flatten_colnames
        df.index = self.flatten_indexnames

        return df

class DataSource:

    def __init__(self, file_path, multi_sheets=True):
        self.file_path = file_path
    
    @functools.cached_property
    def source_file(self):
        # Refreshing Workbook
        print('Refreshing Workbook ...')
        xlapp = win32com.client.DispatchEx("Excel.Application")
        wb = xlapp.workbooks.open(self.file_path)
        wb.RefreshAll()
        wb.Save()
        xlapp.Quit()

        return pd.ExcelFile(self.file_path)
