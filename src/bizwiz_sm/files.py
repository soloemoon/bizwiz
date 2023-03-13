import xlwings as xw
import os
import re
import polars as pl
import pandas as pd
import printable
import duckdb

class files: 
    def __init__(self):
        pass

    def read_multi_file(self, file_path_list=None, concat=False, concat_type = 'diagonal'):
        if concat==True:
            read_files = [pl.read_excel(f, ignore_errors=True) if os.path.splitext(f)[1] == '.xlsx' else pl.read_csv(f, ignore_errors = True) for f in file_path_list]
            output = pl.concat(read_files, how=concat_type)
            return output
        
        elif concat==False:
            for f in self.file_path_list:
                if os.path.splitext(f)[1] == '.xlsx':
                    f1, *other = map(pl.read_excel, file_path_list)
                else:
                    f1, *other = map(pl.read_csv, file_path_list)
            return (f1, *other)
    
    def read_sql_file(self, file_link):
        sql_file = open(file_link, 'r').read().split(';')
        sql_commands = [sc.strip() for sc in sql_file]
        sql_commands = [re.sub("[^{}]+".format(printable), "", sc) for sc in sql_commands]
        return sql_commands
    
    def to_multi_parquet(self, output_directory, df_names, file_path_list = None):
        for f in file_path_list:
            fp = f"{output_directory}{os.path.splitext(f)[0]}.parquet"
            for df in df_names:
                df.write_parquet(fp, compression='zstd')
        return print('Parquet Files Created')
 
    def append_parquet(self, parquet_path, df):
        pq = pl.read_parquet(parquet_path)
        pqf = pl.concat([pq, df], how='diagonal')
        pqf.write_parquet(parquet_path, compression = 'zstd')
        return print("New Data Appended to {}".format(parquet_path)) 

    def query_parquet(self, sql_query, parquet_path):
        # Clean SQL Query
        sql_query = sql_query.lower()
        start = re.findall(r'select.+?from', sql_query)
        end = re.findall(r'(where.*)', sql_query)
        query = " ".join(start) + f" read_parquet({parquet_path}) " + " ".join(end) 
        df = duckdb.query(query).to_df()  
        return df
    
    def dict_from_df(df, key_col, value_col):
        t_dict = df.set_index(key_col).to_dict()[value_col]
        return t_dict

    def export_excel_shts(self, workbook, xl_sheet_list, df_names, index = False):
        app = xw.App(visible = False)
        wb = xw.Book(workbook)
        
        df_dict = dict(zip(xl_sheet_list, df_names))
        
        for sht in xl_sheet_list:
            ws = wb.sheets[sht].clearcontents()
            ws['A1'].options(pd.Dataframe, header=1, index=index, expand = 'table').value = df_dict[sht]
            
        wb.api.RefreshAll()
        wb.save(workbook)
        wb.close()
        app.quit()
   
    
    
