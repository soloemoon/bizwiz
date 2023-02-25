# bizwiz
General purpose business tools to make office life just a bit easier. This package features a series of helper functions to faciliatate common business tasks performed through Python. The package was purposefully developed to be simple, allowing even the least technical users to benefit from the package functionality. 

# Table Formatting and Output
Easily create custom tables with optional sparklines.

```
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
