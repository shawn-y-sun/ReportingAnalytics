import pandas as pd
import numpy as np
from .metrics import Metrics

class Print(Metrics):
    
    indent_l = 42
    indent_r = 10
    line_len = indent_l + indent_r
    sept = "="*line_len
    dash = '-'*line_len

    def __init__(self, dataset, strategy=None, filter=None):
        super().__init__(dataset, strategy, filter)

    def check_val(self, val):
        if isinstance(val, pd.DataFrame):
            return 'df'
        
        elif isinstance(val, (int, float)):
            return 'vals'
        
        elif val == {}:
            return 'empty_dict'
        
        elif isinstance(val, dict):
            vs = list(val.values())
            t1 = type(vs[0])
            same_t = all(isinstance(e, t1) for e in vs)
            any_d = any(isinstance(e, dict) for e in vs)
            
            if any_d:
                return 'dict_dict'
            elif same_t:
                if isinstance(vs[0], pd.DataFrame):
                    return 'dict_dfs'
                else:
                    return 'dict_vals'
            else:
                return 'dict_lines'

        else:
            raise Exception(f'Unaccepted type')

    def form_df(self, dic):
        """Convert a dictionary with values to table"""
        df = pd.DataFrame(list(dic.items()), columns = ['Level', 'Count'])
        df = df.set_index('Level')
        return df

    def add_portion_total(self, df):
        df.index.name = None
        df.replace(np.nan, 0, inplace=True)
        ct_lst = df['Count'].tolist()
        if all([ct <= 1 for ct in ct_lst]):
            return df

        df['Portion'] = df['Count'] / df['Count'].sum() * 100
        df['Portion'] = df['Portion'].map('{:.2f}%'.format)
        try:
            df.loc['Total',:]= df.sum(axis=0, numeric_only=True)
        except TypeError:
            df.index = df.index.astype(str)
            df.loc['Total',:]= df.sum(axis=0, numeric_only=True)
        df['Count'] = df['Count'].astype(int)
        df.replace(np.nan, '', regex=True, inplace=True)

        return df

    def print_line(self, dic):
        for k, v in dic.items():
            k += ':'
            if v is None:
                n = r'*None'
                print(f'{k:<{self.indent_l}}{n:>{self.indent_r}}')
            elif v < 2:
                print(f'{k:<{self.indent_l}}{v:>{self.indent_r}.1%}')
            else:
                print(f'{k:<{self.indent_l}}{v:>{self.indent_r},}')
    
    def print_dfs(self, dic):
        for k, v in dic.items():
            k += ':'
            df = self.add_portion_total(v)
            print(k)
            print(df)
            print(self.dash)

    def print_all(self, dic):
        if isinstance(dic, (int, float)):
            print(dic)
        
        else:
            for key, val in dic.items():
                print(key)
                print(self.sept)

                if val is None or self.check_val(val) == 'empty_dict':
                    print(r"*No Instance")
                    print(self.dash)

                elif self.check_val(val) == 'df':
                    df = self.add_portion_total(val)
                    print(df)
                    print(self.dash)
                
                elif self.check_val(val) == 'vals':
                    self.print_line(dic)
                    print(self.dash)
                    break
                
                elif self.check_val(val) == 'dict_vals':
                    df = self.form_df(val)
                    result = self.add_portion_total(df)
                    print(result)
                    print(self.dash)
                
                elif self.check_val(val) == 'dict_lines':
                    self.print_line(val)
                    print(self.dash)

                elif self.check_val(val) == 'dict_dict':
                    self.print_all(val)
                    print(self.dash)
                
                elif self.check_val(val) == 'dict_dfs':
                    self.print_dfs(val)
                    print(self.dash)

                else:
                    raise Exception("A unknown type")

        print('\n')

    def show(self, metrics = 'all'):
        print(f"{self.sept} {metrics} {self.sept}")
        try:
            result = getattr(self, metrics)
        except AttributeError:
            metrics = input('Please enter a valid metrics name: ')
            self.show(metrics)
        else:
            self.print_all(result)
