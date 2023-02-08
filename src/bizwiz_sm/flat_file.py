class flat_file:
    
    def __init__(self, file_path_list):
        self.file_path_list = file_path_list

    def read_multi_excel(self, concat=False):
       
        if concat == True:
            # Read each file into a list
            read_files = [pl.read_excel(f, ignore_errors = True) for f in self.file_path_list]
    
            output = pl.concat(read_files, how='diagonal')
            return output
        
        elif concat == False:
            f1, *other = map(pl.read_excel, self.file_path_list)
            return (f1, *other)
    
    def read_multi_csv(self, concat=False):
        if concat == True:
            # Read each file into a list
            read_files = [pl.read_csv(f, ignore_errors = True) for f in self.file_path_list]
    
            output_fl = pl.concat(read_files, how='diagonal')
            return output_fl
        
        elif concat == False:
            f1, *other = map(pl.read_csv, self.file_path_list)
            return (f1, *other)
        
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
        
    def read_sql_file(self, file_link):
        sql_file = open(file_link, 'r').read().split(';')
        sql_commands = [sc.strip() for sc in sql_file]
        sql_commands = [re.sub("[^{}]+".format(printable), "", sc) for sc in sql_commands ]
        return sql_commands

    def create_multi_parquet(self, output_directory, df_names):
        for f in self.file_path_list:
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
        df = duckdb.query(sql_query).to_df()  
        return df
    
    def dict_from_df(df, key_col, value_col):
        t_dict = df.set_index(key_col).to_dict()[value_col]
        return t_dict