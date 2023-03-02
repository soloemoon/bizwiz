# bizwiz
NOTE: This package is still a major work in progress!

bizwiz was created to make office life a bit easier. This package contains a helper functions meant to facilitate common business tasks. The simple API enables even the most non-technical users to benefit. 

With bizwiz you can:
* Quickly generate beautiful formatted tables
* Generate advanced Seaborn/Matplotlib Plots
* Efficiently work with flat files, including excel, csv, and parquet
* Send formatted HTML emails with numerous attachments and embedded images


# Tables
Easily create custom tables with optional sparklines using the tables module. Use the default styling (shown below) or customize the table to your hearts content through the helper functions.  

Highlight features:
* Quickly create highly stylized tables
* Automatically generate row level sparklines (more customization coming soon)
* Output your stylized tables to various formats including pdf, powerpoint, and excel (coming soon)
* Embed stylized tables directly into Quarto (coming soon)

Start by importing the tables module
```
from bizwiz import tables
```

## Generate a formatted table
We can pass a dataframe and optionally show sparklines for each row using the create_table initializor. From there we have a series of helper functions to format the table, header, cell, and caption. These are ultimately passed to the `generate_table` function, which also allows us to set the number of decimal places or custom column formatting. Table shown is using default values.

```
# Custom column formatting
col_format = {'sepal_length':'{:.2f}', 'sepal_width':'{:.1f}', 'petal_length':'{:.1f}', 'petal_width':'{:.1f}'}

c = create_table(iris, show_sparklines=True)
table_format = c.table_format()
header_format = c.header_format()   
cell_format = c.cell_format()
caption_format = c.caption_format()

# Creates output Table
c.generate_table(header_format, cell_format, table_format, caption_format, decimals = 1, column_format=col_format)
```
<img width="729" alt="Screen Shot 2023-02-25 at 1 01 31 AM" src="https://user-images.githubusercontent.com/57546826/221343719-61887d0d-8b0e-4e78-abf2-8c88a8217e23.png">

## Easy Table Formatting
Utilize the full suite of pandas styling options in convient helper functions. 
Because this is a pandas styling object, we are able to use the full array of options available. Multiple helper functions are included to make adding column bars, highlighting values, and more incredibly simple.
 
 ```
col_colors = {'sepal_width':'blue', 'sepal_length':'lightgreen'}
c.column_bar(col_colors, align='left')
 ```
 <img width="729" alt="Screen Shot 2023-02-25 at 1 01 56 AM" src="https://user-images.githubusercontent.com/57546826/221343808-10a429d8-39cc-4028-8e28-6b1449a0ff6d.png">
 

# Charts
Quickly create a number of advanced Seaborn/Matplotlib charts with the use of these helper functions. 

Create:
* heatmaps
* dot plots
* funnel charts
* horizontal bar graphs
* multi-chart timeseries

Start by importing the tables module
```
from bizwiz import bizcharts
```

# Funnel Chart
```
t=pd.DataFrame(data={'value1':[80,73,58,42,23,15], 'category':['A', 'B', 'C', 'D', 'E', 'F']})

bizcharts(t).funnel_chart(x_col='value1', label_col='category')
```
<img width="751" alt="Screen Shot 2023-03-01 at 7 09 18 PM" src="https://user-images.githubusercontent.com/57546826/222304817-0a2cdc1a-8f1a-4ec3-aa67-202c9e3174c6.png">

# Bullet Graph
Based on code provided by Chris Moffit of pbpython.com. 
```
data_to_plot2 = [("User 1", 105, 120),
                 ("User 2", 99, 110),
                 ("User 3", 109, 125),
                 ("User 4", 135, 123),
                 ("User 5", 45, 105)]
                 
bizcharts(data_to_plot2).bullet_graph(limits=[20, 60, 100, 160],labels=["Poor", "OK", "Good", "Excellent"], size=(8,5), axis_label="Metric", title="Performance")

```
![image](https://user-images.githubusercontent.com/57546826/222305119-d21ec214-73ad-43e8-ad2f-0a868154d47f.png)

# Flat Files
This module is primarily built on top of polars and xlWings ensuring speed, even when working with the largest of files. 

Highlight Features:
* Read multiple excel or csv files into multiple dataframes or a single dataframe.
* Export multiple excel sheets to a workbook
* Ingest and automatically clean a .sql file
* Create multiple parquet files from several flat files
* Append multiple flat files into a single parquet file
* Write SQL to query a parquet file

Start by importing the flat_file module.
```
from bizwiz import flat_file
```

## Working with multiple flat files
Read multiple excel or csv files into multiple dataframes or a single dataframe. Output dataframe(s) to multiple parquet files, append to an existing parquet file, or create a single new parquet file.
```
# Initialize module with a list of file paths that you'll be working with
ff = flat_file(file_path_list)

# Read in two excel files based on the file path list
xl1, xl2 = ff.read_multi_excel(concat=False)

# Create multiple parquet files from the ingested excel
ff.create_multi_parquet(output_directory, [xl1, xl2])
```

## Export multiple excel sheets to a single workbook
Quickly export multiple dataframes to multiple excel sheets in a single workbook. Only one line of code is needed.
```
# Define Parameters
workbook_path = 'file path here'
sheet_list = ['Sheet 1', 'Sheet 2']
df_names = [xl1, xl2]

ff = flat_file()
ff.export_excel_shts(workbook_path, sheet_list, df_names
```

## Reading a .SQL File
Reading in a cleaned .sql file for execution in a single line of code. This is safer and more efficient than maintaing sql queries in code. 
```
ff = flat_file()
# read in a .sql file and execute it
sql_file = ff.read_sql_file(file_path)
conn = pyodbc.connect()
df = pd.read_sql_query(sql_file, conn)
```

## Query an existing parquet file
No need to define the table name in the query. Just pass the file path and bizwiz takes care of the rest.
```
ff = flat_file()
results = ff.query_parquet(sql, parquet_path)
```
sql = 'select * from where year > 2005'
parquet_path = 'file path here'
```
