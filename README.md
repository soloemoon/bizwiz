# bizwiz
NOTE: This package is still a major work in progress!

bizwiz was created to make office life a bit easier. This package contains a helper functions meant to facilitate common business tasks. The simple API enables even the most non-technical users to benefit. 

With bizwiz you can:
* Quickly generate beautiful formatted tables
* Efficiently work with flat files, including excel, csv, and parquet
* Send formatted HTML emails with numerous attachments and embedded images

# Tables
Easily create custom tables with optional sparklines using the tables module. Use the default styling (shown below) or customize the table to your hearts content through the helper functions.  

```
from bizwiz import tables

c = create_table(iris, show_sparklines=True)
table_format = c.table_format()
header_format = c.header_format()   
cell_format = c.cell_format()
caption_format = c.caption_format()

# Creates output Table
c.generate_table(header_format, cell_format, table_format, caption_format, decimals = 1, column_format=col_format)
```
<img width="729" alt="Screen Shot 2023-02-25 at 1 01 31 AM" src="https://user-images.githubusercontent.com/57546826/221343719-61887d0d-8b0e-4e78-abf2-8c88a8217e23.png">

 Utilize the full suite of pandas styling options in convient helper functions. 
 
 ```
col_colors = {'sepal_width':'blue', 'sepal_length':'lightgreen'}
c.column_bar(col_colors, align='left')
 ```
 <img width="729" alt="Screen Shot 2023-02-25 at 1 01 56 AM" src="https://user-images.githubusercontent.com/57546826/221343808-10a429d8-39cc-4028-8e28-6b1449a0ff6d.png">

# Flat Files
This module is primarily built on top of polars and xlWings ensuring speed, even when working with the largest of files. 

Core Features:
* Read multiple excel or csv files into multiple dataframes or a single dataframe
* Export multiple excel sheets to a workbook
* Ingest and automatically clean a .sql file
* Create multiple parquet files from several flat files
* Append multiple flat files into a single parquet file
* Write SQL to query a parquet file

```
from bizwiz import flat_file

# Initialize module with a list of file paths that you'll be working with
ff = flat_file(file_path_list)

# Read in two excel files based on the file path list
xl1, xl2 = ff.read_multi_excel(concat=True)

# Create multiple parquet files from the ingested excel
ff.create_multi_parquet(output_directory, [xl1, xl2])

# read in a .sql file and execute it
sql_file = ff.read_sql_file(file_path)
conn = pyodbc.connect()
df = pd.read_sql_query(sql_file, conn)
```
