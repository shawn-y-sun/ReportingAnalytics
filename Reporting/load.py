import pandas as pd
import os
from tkinter.filedialog import askopenfilename
from functools import lru_cache
import warnings

@lru_cache(maxsize=5)
def load_data(file_name=None, **kwargs):
    """Returns a pandas dataframe

    Keyword Arguments:
    file_name (optional) -- absolute or relative path of a .csv or .xlsx file 
        (if not provided, then a pop-up window allows you to select file)
    kwargs (optional) -- dictionary of optional arguments that can be read by 
        pd.read_csv() and pd.read_excel()
    """
    warnings.filterwarnings('ignore')
    
    if file_name is None:
        file_name = askopenfilename()
    ext = os.path.splitext(file_name)[1]

    print("Reading File ...")
    if ext == ".csv":
        return pd.read_csv(file_name, **kwargs)

    elif ext == ".xlsx":
        return pd.read_excel(file_name, **kwargs)

    else:
        raise Exception("Please choose a CSV or Excel file")

if __name__ == '__main__':
    load_data()
