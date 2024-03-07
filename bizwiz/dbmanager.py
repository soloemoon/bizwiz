import pyodbc
import pandas as pd
import re
import sqlparse
import printable

def odbconnect(dsn_name='redshift'):
    db_conn = pyodbc.connect(DSN=dsn_name, autocommit=True)
    return db_conn

def execute_query_file(query, db_conn):
    
    if query.endswith('.sql') == True:
        
        sql_commands = open(query, 'r').read().strip().split(';')
        sql_commands = [x.strip() for x in sql_commands]
        sql_commands = [re.sub("[^{}]+".format(printable), "", x) for x in sql_commands]
        sql_commands = [sqlparse.format(x, strip_comments=True).strip for x in sql_commands]
                      
    else:
        pass
    
    pd.io.sql.execute(query, db_conn)
    
    return print('Query Successfully Run')


def querydb(query, db_conn):
    
    if query.endswith('.sql')==True:
        query=open(query, 'r').read().strip()
        query = sqlparse.format(query, strip_comments=True).strip()
        query = re.sub("[^{}]+".format(printable), "", query)
    else:
        pass
    
    result = pd.read_sql(query, db_conn)
    
    return result
    

def create_table_from_df(df, table_name, db_conn):
    
    # Drop The Existing Table
    drop_table = f'drop table if exists {table_name};'
    pd.io.sql.execute(drop_table, db_conn)
    print(table_name + ': Drop Completed')
    
    # Clean dataframe names
    df = clean_names(df)
    value_list = [str(x) for x in df.values.tolist()]
    
    # Clean columns
    columns = [str(x) for x in df.columns.tolist()]
    
    list(df.columns)
    columns = str(columns)
    
    columns = (
        columns
        .replace("',"," varchar(1000),")
        .replace("']"," varchar(1000)")
        .replace("[","")
        .replace("]","")
        .replace("'","")
        )
    
    # Create table
    create_table = f'create table if not exists {table_name}({columns});'
    pd.io.sql.execute(create_table, db_conn)
    print(table_name + ': created successfully')
    
    # Insert in chunks
    step = 10000

    def clean_value(v):
        v = (
            v
            .replace('[', '(')
            .replace(']', ')')
            .replace('((', '(')
            .replace('))', ')')
        )
        return v
    
    value_list = [clean_value(x) for x in value_list]

    
    for i in range( 0, len(value_list) ):
        x=i
        res = value_list[x:x+step]
        insert_statement = f'insert into {table_name} values {res}'
        x=str(insert_statement)

        pd.io.sql.execute(x, db_conn)
        
        print(table_name + ' : rows inserted')
        
    def create_aws_table(df, table_name, db_conn,grant_table_access = False, aws_group=False):

        create_table_from_df(df, table_name, db_conn)

        if grant_table_access != False:
            grant = f'grant all on table {table_name} to group {aws_group}'
            pd.io.sql.execute(grant, db_conn)
            print('grant statement run')
        