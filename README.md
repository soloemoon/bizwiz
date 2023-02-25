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
