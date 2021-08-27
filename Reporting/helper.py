from win32com.client import DispatchEx
import openpyxl
import traceback

def move_sheets(source_path, dest_path):
    excel = DispatchEx('Excel.Application')
    excel.AskToUpdateLinks = False
    excel.EnableEvents = False
    excel.DisplayAlerts = False

    wb_s = excel.Workbooks.Open(source_path)
    wb_d = excel.Workbooks.Open(dest_path)

    sheet_names = [sheet.Name for sheet in wb_s.Sheets]
    wb_s.Worksheets.Add(After=wb_s.Sheets(sheet_names[-1]))

    for sheet in sheet_names:
        ws = wb_s.Worksheets(sheet)
        ws.Move(None, After=wb_d.Sheets(wb_d.Sheets.count))

    wb_d.Close(SaveChanges=True)
    wb_s.Close(SaveChanges=True)
    
    excel.Quit()
    del excel

def hide_tabs(file_path, unhidden=None, hidden=None):
    xls_book = openpyxl.load_workbook(filename=file_path)
    sheet_names = xls_book.get_sheet_names()

    for sheet in sheet_names:
        xls_sheet = xls_book.get_sheet_by_name(sheet)

        if unhidden is not None:
            if sheet not in unhidden:
                xls_sheet.sheet_state = 'hidden'
        elif hidden is not None:
            if sheet in hidden:
                xls_sheet.sheet_state = 'hidden'
    
    xls_book.save(file_path)



class Slicer:

    def __init__(self, name, target_sheet, target_cell, pivotsheet, pivottable, field, height_scale=1, width_scale=1):
        self.name = name
        self.target_sheet = target_sheet
        self.target_cell = target_cell
        self.pivotsheet = pivotsheet
        self.pivottable = pivottable
        self.field = field
        self.height_scale = height_scale
        self.width_scale = width_scale

class Slicers:

    def __init__(self):
        self.slicers = []
    
    def __add__(self, slicer):
        if isinstance(slicer, Slicer):
            self.slicers.append(slicer)
        elif isinstance(slicer, Slicers):
            self.slicers.extend(slicer.slicers)

    def add(self, file_path):
        excel = DispatchEx('Excel.Application')

        wb = excel.Workbooks.Open(file_path)
    
        for sc in wb.SlicerCaches:
            sc.Delete
        
        for index, sc in enumerate(self.slicers):
            pivotsheet = sc.pivotsheet
            dbsheet = sc.target_sheet
            ws_pvt = wb.Worksheets(pivotsheet)
            ws_db = wb.Worksheets(dbsheet)

            pvt = ws_pvt.PivotTables(sc.pivottable)

            field_name = sc.field
            caption = sc.name
            s_range = sc.target_cell
            s_top = ws_db.Range(s_range).Top
            s_left = ws_db.Range(s_range).Left
            s_height_scale = sc.height_scale
            s_width_scale = sc.width_scale

            # Refresh PivotTables
            pvt.PivotCache().Refresh()

            # Add Slicers
            try:
                slcache = wb.SlicerCaches.Add(pvt, field_name, f'SLcache{index}')
                slicer = slcache.Slicers.Add(ws_db)

                slicer.Name = f'Slicer{index}'
                slicer.Caption = caption
                slicer.Top = s_top
                slicer.Left = s_left
                slicer.Height = slicer.Height * s_height_scale
                slicer.Width = slicer.Width * s_width_scale
            except:
                print(f'error{index}')
                traceback.print_exc()
                continue

        wb.Close(SaveChanges=True)
        excel.Quit()
        del excel


sl_new_v3 = Slicers()

# Distributions Slicers
sl_new_v3 + Slicer('Status (Tier)', 'Distributions Charts', 'P3', 'Distributions_Helper', 'dist_status_tier', 'Status', 1.23, 1.2)
sl_new_v3 + Slicer('Status (BCN)', 'Distributions Charts', 'P25', 'Distributions_Helper', 'dist_status_bcn', 'Status', 1.23, 1.2)
sl_new_v3 + Slicer('Tier (BCN)', 'Distributions Charts', 'P42', 'Distributions_Helper', 'dist_tier_bcn', 'BCN Tiers', 0.6)
sl_new_v3 + Slicer('Status (BNI)', 'Distributions Charts', 'P56', 'Distributions_Helper', 'dist_status_bni', 'Status', 1.23, 1.2)
sl_new_v3 + Slicer('Tier (BNI)', 'Distributions Charts', 'P73', 'Distributions_Helper', 'dist_tier_bni', 'BNI Tiers', 0.6)
sl_new_v3 + Slicer('Status (CScore)', 'Distributions Charts', 'P87', 'Distributions_Helper', 'dist_status_cs', 'Status', 1.23, 1.2)
sl_new_v3 + Slicer('Tier (CScore)', 'Distributions Charts', 'P104', 'Distributions_Helper', 'dist_tier_cs', 'CScore Tiers', 0.6)

# Profiles Slicers
sl_new_v3 + Slicer('Tier - 1', 'Profiles Dashboard', 'F3', 'Profiles_Helper', 'pf_tier_1', 'Tier', 0.6)
sl_new_v3 + Slicer('Tier - 2', 'Profiles Dashboard', 'I3', 'Profiles_Helper', 'pf_tier_2', 'Tier', 0.6)
sl_new_v3 + Slicer('Status - 1', 'Profiles Dashboard', 'F9', 'Profiles_Helper', 'pf_status_1', 'Status', 1.23)
sl_new_v3 + Slicer('Status - 2', 'Profiles Dashboard', 'I9', 'Profiles_Helper', 'pf_status_2', 'Status', 1.23)
sl_new_v3 + Slicer('Time - 1', 'Profiles Dashboard', 'F18', 'Profiles_Helper', 'pf_time_1', 'Time', 2)
sl_new_v3 + Slicer('Time - 2', 'Profiles Dashboard', 'I18', 'Profiles_Helper', 'pf_time_2', 'Time', 2)

sl_new_v3 + Slicer('Status - Chart', 'Profiles Dashboard', 'U16', 'Profiles_Helper', 'pf_status_chart', 'Status', 1.23)
sl_new_v3 + Slicer('Metric - Chart', 'Profiles Dashboard', 'X16', 'Profiles_Helper', 'pf_metrics_chart', 'Metric', 2)
sl_new_v3 + Slicer('Tier - Chart', 'Profiles Dashboard', 'AA16', 'Profiles_Helper', 'pf_tier_chart', 'Tier', 0.6)