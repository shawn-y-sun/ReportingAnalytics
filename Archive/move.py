from win32com.client import DispatchEx
import time


source_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report\New Report Charts.xlsx'
dest_path = r'C:\Users\sunsh\Documents\Daily Approval Report\Report\New Report_strat_v2.xlsx'
excel = DispatchEx('Excel.Application')
excel.Visible = True
excel.AskToUpdateLinks = False
excel.EnableEvents = False
excel.DisplayAlerts = False

wb_s = excel.Workbooks.Open(source_path)
wb_d = excel.Workbooks.Open(dest_path)

# sheet_names = [sheet.Name for sheet in wb_s.Sheets]
# wb_s.Worksheets.Add(After=wb_s.Sheets(sheet_names[-1]))

# for sheet in sheet_names:
#     ws = wb_s.Worksheets(sheet)
#     ws.Move(After=wb_d.Sheets(wb_d.Sheets.count))

ws = wb_s.Worksheets(1)
ws.Move(None, After=wb_d.Worksheets(1))

ws = wb_s.Worksheets(1)
ws.Move(None, After=wb_d.Worksheets(1))

wb_d.Close(SaveChanges=True)
wb_s.Close(SaveChanges=True)

excel.Quit()
del excel