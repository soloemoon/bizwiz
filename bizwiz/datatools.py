from typing import Dict, Union

import pandas_flavor as pf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def _date_range_calc(start_date, end_date, number_of_days, date_format='%Y-%m-%d'):
# Helper function to calculate date range
    start_date = datetime.striptime(start_date, date_format)
    end_date = datetime.striptime(end_date, date_format)
    
    dl = pd.period_range(
        start_date,
        end_date,
        periods=number_of_days
        )
    dl = sorted(dl)

    return dl    

def create_date_list( 
    start_date: str, 
    end_date: str, 
    number_of_days: int=1, 
    date_format: str='%Y-%m-%d', 
    remove_weekends: bool=False
) -> list:
    
    """Creates a list of dates between a specified start and end date based on a defined interval.

        Weekends can be removed by setting the remove_weekends parameter to True.

        Examples:
            Functional usage

            >>> import pandas as pd
            >>> from bizwiz import datatools as dt
            >>> days = dt.create_date_list(
            ...     start_date = '2023-01-01'
            ...     end_date = '2023-12-01
            ...     number_of_days = 1
            ...     date_format = '%Y-%m-%d'
            ...     remove_weekends: True
            ... )  # doctest: +SKIP


        Args:
            start_date: Beginning date of the sequence
            end_date: Ending date of the sequence
            number_of_days: Number of days to increment by
            date_format: datetime compatible date format. Default is %Y-%m-%d e.g. '2024-01-31'
            remove_weekends: Dictates if calendar days or business days are displayed. Default is False (calendar days)

        Returns:
            List of days between the defined start and end dates.
    """
       
    date_list = _date_range_calc(start_date, end_date, number_of_days, date_format)
    
    if remove_weekends == True:
        date_list = [x.strftime(date_format) for x in date_list]
        
    # remove holidays coming soon - user input list or default to US public holidays
    date_list = [x.strftime(date_format) for x in date_list]

    return date_list
    
def create_month_list(
    start_date: str, 
    end_date: str, 
    date_format: str='%Y-%m-%d'
) -> list:
    
    """Creates a list of months between a specified start and end date.

        Months displayed as of the first day of the month. E.G. 2024-10-01

        Examples:
            Functional usage

            >>> import pandas as pd
            >>> from bizwiz import datatools as dt
            >>> days = dt.create_monthlist(
            ...     start_date = '2023-01-01'
            ...     end_date = '2023-12-01
            ...     date_format = '%Y-%m-%d'
            ... )  # doctest: +SKIP

        Args:
            start_date: Beginning date of the sequence
            end_date: Ending date of the sequence
            date_format: datetime compatible date format. Default is %Y-%m-%d e.g. '2024-01-31'

        Returns:
            List of days between the defined start and end dates.
    """
    
    date_list = _date_range_calc(start_date, end_date, date_format)
    date_list = date_list[date_list.day==1]
    date_list = sorted(date_list)
    date_list = [x.strftime(date_format) for x in date_list]

    return date_list

def _business_days(start_date, end_date):
    # if the start date is on a weekend, forward the date to next Monday
    WEEKDAY_FRIDAY = 4 
    
    if start_date.weekday() > WEEKDAY_FRIDAY:
        start_date = start_date + timedelta( days=7 - start_date.weekday() )

    # if the end date is on a weekend, rewind the date to the previous Friday
    if end_date.weekday() > WEEKDAY_FRIDAY:
        end_date = end_date - timedelta( days=end_date.weekday() - WEEKDAY_FRIDAY )

    if start_date > end_date:
        return 0
    # that makes the difference easy, no remainders etc
    diff_days = (end_date - start_date).days + 1
    weeks = int(diff_days / 7)

    remainder = end_date.weekday() - start_date.weekday() + 1

    if remainder != 0 and end_date.weekday() < start_date.weekday():
        remainder = 5 + remainder
        
    return weeks * 5 + remainder

@pf.register_dataframe_method
def date_diff(
    df: pd.DataFrame, 
    start_date_column: str, 
    end_date_column: str, 
    date_format: str = '%Y-%m-%d', 
    calculation: str='days'
) -> pd.DataFrame:
        
    """Computes the difference between two dataframe date columns in calendar/business days, months, or years.

        If date columns are formatted as strings then they are converted to datetime objects.

        Examples:
            Functional usage

            >>> import pandas as pd
            >>> from bizwiz import datatools as dt
            >>> df = df.dt.datediff(
            ...     start_date_column = 'initial dates'
            ...     end_date_column = 'ending dates'
            ...     date_format = '%Y-%m-%d'
            ...     calculation = 'day'
            ... )  # doctest: +SKIP


        Args:
            df: DataFrame containing the date columns to be differenced
            start_date_column: Name of the column containing the initial dates
            end_date_column: Name of the column containing the ending dates
            date_format: datetime compatible date format. Default is %Y-%m-%d e.g. '2024-01-31'
            calculation: Differencing calculation. Default is day, which adds both calendar and business days to dataframe.
                Options are days, months, years

        Returns:
            DataFrame that has date differenced columns.
    """
    start_list = [pd.to_datetime(x) for x in df[start_date_column].tolist()]
    end_list = [pd.to_datetime(x) for x in df[end_date_column].tolist()]

    calculation = calculation.lower()

    if calculation in['day', 'd', 'days']:
        calendar_diff_list = [(x - y).days for x, y in zip(end_list, start_list)]
        business_day_diff_list = [_business_days(x, y) for x,y in zip(start_list, end_list)]

        df['date_diff_calendar_days'] = calendar_diff_list
        df['date_diff_business_days'] = business_day_diff_list
        
    elif calculation in['month', 'months']:
        month_diff_list = [(x.year - y.year) * 12 + x.month - y.month for x, y in zip(end_list, start_list)]

        df['date_diff_months']  = month_diff_list
        
    elif calculation in['year', 'years']:
        year_diff_list = [(x.year - y.year) for x, y in zip(end_list, start_list)]

        df['date_diff_years']  = year_diff_list
             
    return df


@pf.register_dataframe_method
def dict_from_df(
    df: pd.DataFrame, 
    key_column: str, 
    value_column: str
) -> dict:

    """Create a dictionary from dataframe columns

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import datatools as dt
                >>> df = df.dict_from_df(
                ... key_column = 'A'
                ... value_column = 'B'
                ... )  # doctest: +SKIP


            Args:
                df: Primary dataframe
                key_column: Column name containing the values to be used dictionary keys
                value_column: Column name containing the values to be used as dictionary values
                
            Returns:
                Dictionary with key, value combinations based on dataframe columns
            """
        
    t_dict = df.set_index(key_column).to_dict()[value_column]

    return t_dict

@pf.register_dataframe_method
def retain_leading_zero(
    df: pd.DataFrame, 
    column_names:list
):

    if isinstance(column_names) == str:
        column_names = list(column_names)

    for col in column_names:
        df[col] = df[col].apply('="{}"'.format)

    return df

@pf.register_dataframe_method
def fill_leading_zero(
    df: pd.DataFrame, 
    column_names: str, 
    character_length: int=10
) -> pd.DataFrame:

    df[column_names] = df[column_names].astype(str).str.zfill(character_length)
    
    return df

@pf.register_dataframe_method
def subset_by_group(
    df: pd.DataFrame, 
    column_name: str
) -> dict:

    return dict(iter(df.groupby(column_name)))

@pf.register_dataframe_method
def dataframe_compare(
    df: pd.DataFrame, 
    df2: pd.DataFrame,
) -> pd.DataFrame:
        
    """Compare two dataframes and output a dataframe of values that changed.

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import datatools as dt
                >>> df = df.dataframe_compare(df2
                ... )  # doctest: +SKIP


            Args:
                df: Primary dataframe
                df2: dataframe to be compared to the primary
                

            Returns:
                DataFrame that has breakdown of the values that changed
    """
    
    ne_stacked = (df != df2).stack()
    changed = ne_stacked[ne_stacked]
    changed.index.names = ['id', 'col']
    difference_locations = np.where(df != df2)
    changed_from = df.values[difference_locations]
    changed_to = df2.values[difference_locations]
    result = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)
    return result

@pf.register_dataframe_method
def unique_records_between_df(
    df: pd.DataFrame, 
    df2: pd.DataFrame, 
    column_names: list
) -> pd.DataFrame:
    """Get the unique records between two like dataframe columns

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import datatools as dt
                >>> df = df['lookup_column'].create_flag(
                ...     flag_name = 'mapped_values',
                ...     lookup_list = ['A', 'B', 'C']
                ...     map_if_in_list = True
                ... )  # doctest: +SKIP


            Args:
                df: DataFrame containing the data to map
                df2: 
                column_names:
                

            Returns:
                DataFrame that has date differenced columns.
    """
    
    if isinstance(column_names) == str:
        column_names = list(column_names)

    result = pd.merge(df, df2, on=column_names, how = 'outer', indicator=True)
    result = result[result._merge != 'both'] # Filter out records from both

    return result

@pf.register_dataframe_method
def create_flag(
        df: pd.DataFrame, 
        lookup_column: str, 
        flag_name: str, 
        lookup_list: list, 
        overwrite_values: bool = True, 
        default_value: str = 'N', 
        flag_value: str = 'Y',
        map_if_in_list: bool = True
) -> pd.DataFrame:

    """Creates a flag column in dataframe based on the values in a list. Values can be mapped based on either being present in the list or not being present in the list.

        Examples:
            Functional usage

            >>> import pandas as pd
            >>> from bizwiz import datatools as dt
            >>> df = df['lookup_column'].create_flag(
            ...     flag_name = 'mapped_values',
            ...     lookup_list = ['A', 'B', 'C']
            ...     map_if_in_list = True
            ... )  # doctest: +SKIP


        Args:
            df: DataFrame containing the data to map
            lookup_column: Column name containing the values to compare against the list
            flag_name: Desired output column name of the mapped flag
            lookup_list: List of values to be compared against dataframe for mapping
            overwrite_values: Boolean that determines if the default value (N) will be used as flag or if the original column values will be maintained. Default is True.
            default_value: The default value if the flag is missing. Currently 'N'
            flag_value: The value to return if a mapping is possible. Default is 'Y'
            map_if_in_list: Set to true to map the values if they exist in the inputted list. Select false to map the values if they are not in the list.
            

        Returns:
            DataFrame that has a generated flag column.
        """

    if overwrite_values == True:
        df[flag_name] = default_value
    
    if map_if_in_list  == True:
        df.loc[(df[lookup_column].isin(lookup_list)), flag_name] = flag_value
    
    elif map_if_in_list == False:
        df.loc[~(df[lookup_column].isin(lookup_list)), flag_name] = flag_value
    
    return df
