




def __csv_read(path, **kwargs):
    csv_encodings = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'latin1', 'cpl1252']
    
    for e in csv_encodings:
        try:
            temp = (
                 pd.read_csv(path, encoding=e, engine='pyarrow',dtype_backend='pyarrow', **kwargs)
                 .clean_names()
                 .remove_empty
            )
        
        except Exception as e:
            pass
        
    return temp

def __xl_read(path, **kwargs):
    temp =(
        pd.read_excel(path, dtype_backend='arrow', **kwargs)
        .clean_names()
        .remove_empty()
        )
    return temp

def bulk_read_excel(
          file_path_list: list, 
          concat: bool=True,  
          **kwargs
        ):
    
    xlsx_files = [f for f in file_path_list if fnmatch(f, '*.xls?')]
    
    if concat==True:  
        result = pd.concat([__xl_read(f, **kwargs) for f in xlsx_files])
    
    elif concat == False:
        result, *other = map(__xl_read, file_path_list)
    
    return (result, *other)

    
def bulk_read_csv(file_path_list, concat=True, **kwargs):
    
    csv_files = [file for file in file_path_list if fnmatch(file, '*.csv')]
    
    if concat==True:
        
        result = pd.concat([__csv_read(f, **kwargs) for f in csv_files])
        
    elif concat == False:
        
        result, *other = map(__csv_read, file_path_list)
    
    return (result, *other)


def query_parquet(sql_query, parquet_path):
   
        sql_query = sql_query.lower()
        start = re.findall(r'select.+?from', sql_query)
        end = re.findall(r'(where.*)', sql_query)
        query = " ".join(start) + f" read_parquet({parquet_path}) " + " ".join(end) 
        df = duckdb.query(query).to_df()  
        return df
    
def export_multi_parquet(output_directory, df_names, file_path_list = None):
        for f in file_path_list:
            fp = f"{output_directory}{os.path.splitext(f)[0]}.parquet"
            for df in df_names:
                df.write_parquet(fp, compression='zstd')
        return print('Parquet Files Created')


@pf.register_dataframe_method
def append_parquet(df, parquet_path):
        pq = pd.read_parquet(parquet_path)
        pqf = pd.concat([pq, df])
        pqf.write_parquet(parquet_path, compression = 'zstd')
        return print("New Data Appended to {}".format(parquet_path)) 

def export_multi_sheet_excel(df_to_sheet_dict, workbook_name = 'new_workbook.xlsx'):
    wb = xw.Book(workbook_name)
    
    for k, v in df_to_sheet_dict.items():
        wb.sheets.add(name=v)
        wb.sheets[v].range('A1').value= k
        wb.sheets[v].reange('A1').options(pd.DataFrame, expand='table').value
        
    for ws in wb.sheets:
        ws.autofit(axis='columns')
    
    wb.save()
    return print('workbook output')