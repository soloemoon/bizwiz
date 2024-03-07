def __csv_read(path, **kwargs):
    csv_encodings = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'latin1', 'cpl1252']
    
    for e in csv_encodings:
        try:
            temp = pl.read_csv(path, encoding=e, **kwargs)
        
        except Exception as e:
            pass
        
    return temp

def __xl_read(path, **kwargs):
    temp =(
        pl.read_excel(path, **kwargs)
        .to_pandas(use_pyarrow_extension_array=True)
        .clean_names()
        .remove_empty()
        )
    return temp

def bulk_read_excel(file_path_list, concat=True, concat_type='diagonal',  **kwargs):
    
    xlsx_files = [file for file in file_paths if fnmatch(file, '*.xls?')]
    
    if concat==True:
        
        read_files = [pl.read_excel(f, **kwargs) for f in xlsx_files]
        result = (
            pl.concat(read_files, how=concat_type)
            .to_pandas(use_pyarrow_extension_array=True)
            .clean_names()
            .remove_empty()
            )
    
    elif concat == False:
        
        result, *other = map(__xl_read, file_path_list)
    
    return (result, *other)

    
def bulk_read_csv(file_path_list, concat=True, concat_type='diagonal', return_pandas_df = True, **kwargs):
    
    csv_files = [file for file in file_paths if fnmatch(file, '*.csv')]
    
    if concat==True:
        
        read_files = [__csv_read(f, **kwargs) for f in csv_files]
        result = pl.concat(read_files, how=concat_type)
        
        if return_pandas_df == True:
            result = (
                result
                .to_pandas(use_pyarrow_extension_array=True)
                .clean_names()
                .remove_empty
                      )
    
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
 
    
def append_parquet(parquet_path, df):
        pq = pl.read_parquet(parquet_path)
        pqf = pl.concat([pq, df], how='diagonal')
        pqf.write_parquet(parquet_path, compression = 'zstd')
        return print("New Data Appended to {}".format(parquet_path)) 


def dict_from_df(df, key_col, value_col):
        t_dict = df.set_index(key_col).to_dict()[value_col]
        return t_dict
    


def retain_leading_zero(df, column_names):
    if isinstance(column_names, list):
        for col in column_names:
            df[col] = '="' + df[col] +'"'
    
    if isinstance(column_names, str):
        df[col] = '="' + df[col] +'"'
    
    return df

def fill_leading_zero(df, column_names, character_length=10):
    df[column_names] = df[column_names].astype(str).str.zfill(character_length)
    return df


def export_multi_sheet_excel(df_to_sheet_dict, workbook_name = 'new_workbook.xlsx'):
    wb = xw.Book(output)
    
    for k, v in df_to_sheet_dict.items():
        wb.sheets.add(name=v)
        wb.sheets[v].range('A1').value= k
        wb.sheets[v].reange('A1').options(pd.DataFrame, expand='table').value
        
    for ws in wb.sheets:
        ws.autofit(axis='columns')
    
    wb.save()
    return print('workbook output')

def __date_range_calc(start_date, end_date, number_of_days, date_format='%Y-%m-%d'):
    start_date = datetime.striptime(start_date, date_format)
    end_date = datetime.striptime(end_date, date_format)
    
    dl = pl.datetime_range(
        start_date,
        end_date,
        timedelta(days=number_of_days),
        eager=True
        ).alias('date')
    dl = sorted(dl)
    return dl
        

def create_date_list(start_date, end_date, number_of_days=1, date_format='%Y-%m-%d', remove_weekends=False):
    date_list = __date_range_calc(start_date, end_date, number_of_days, date_format)
    
    if remove_weekends == True:
        date_list = [x.strftime(date_format) for x in date_list]
        
    # remove holidays
    date_list = [x.strftime(date_format) for x in date_list]
    return date_list
    
def create_month_list(start_date, end_date, date_format='%Y-%m-%d'):
    date_list = __date_range_calc(start_date, end_date, date_format)
    date_list = date_list[date_list.day==1]
    date_list = sorted(date_list)
    date_list = [x.strftime(date_format) for x in date_list]
    return date_list

def __business_days(start_date, end_date):
    # if the start date is on a weekend, forward the date to next Monday
    WEEKDAY_FRIDAY = 4 
    
    if start_date.weekday() > WEEKDAY_FRIDAY:
        start_date = start_date + timedelta(days=7 - start_date.weekday())

    # if the end date is on a weekend, rewind the date to the previous Friday
    if end_date.weekday() > WEEKDAY_FRIDAY:
        end_date = end_date - timedelta(days=end_date.weekday() - WEEKDAY_FRIDAY)

    if start_date > end_date:
        return 0
    # that makes the difference easy, no remainders etc
    diff_days = (end_date - start_date).days + 1
    weeks = int(diff_days / 7)

    remainder = end_date.weekday() - start_date.weekday() + 1

    if remainder != 0 and end_date.weekday() < start_date.weekday():
        remainder = 5 + remainder
    
    result = weeks * 5 + remainder
        
    return result


def date_diff(df, start_date, end_date, date_format = '%Y-%m-%d', output_column_name='date_diff', calculation='calendar days'):
    
    calculation = calculation.lower()
    
    df[start_date] = pd.to_datetime(df[start_date], format = date_format)
    df[end_date] = pd.to_datetime(df[end_date], format=date_format)
    
    if calculation == 'calendar days':
        df[output_column_name] = (df[end_date] - df[start_date]).dt.days
            
        
    elif calculation == 'business days':
        df[output_column_name] = df.apply(lambda x: __business_days(x[start_date], x[end_date]), axis=1).tolist()
        
    return df


        
        
    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    