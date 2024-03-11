import pandas_flavor as pf
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns


@pf.register_dataframe_method
def bullet_graph(
    df: pd.DataFrame, 
    category_column: str, 
    category_value_column: str, 
    target_value_column: str, 
    limits: list=[20, 40, 80, 100], 
    labels: list=['Poor', 'Ok', 'Good', 'Excellent'], 
    axis_label: str='Metric', 
    title: str='Bullet Graph',
    size: tuple=(5, 3), 
    palette_color: str='green', 
    formatter: str=None, 
    target_color: str="gray",
    bar_color: str="black", 
    label_color: str="black"
    ):
        """Create bullet chart based on dataframe values.

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import charter
                >>> df.bullet_graph(
                ... category_column = 'category', 
                ... category_value_column='category_val', 
                ... target_value_column='target_val', 
                ... limits=[20, 40, 80, 100]
                ... )  # doctest: +SKIP


            Args:
                df: dataframe containing chart data
                category_column: Column name of the category value
                category_value_column: Column name of the values associated with the category
                target_value_column: Column name of the values that are targeted for the category column
                limits: List of x axis values. e.g. [100, 120, 140, 150]
                labels: List of values associated with what the limits mean. e.g. [Poor, ok, good, excellent]
                axis_label: X axis label name. Default is Metric.
                title: Chart title
                size: Size of chart
                palette_color: Diverging color to apply to the chart. Default is green. Lighter to Darker.
                formatter: formats tick as string
                target_color: Color of the target variable
                bar_color: Color of the bars
                label_color: Color of the labelss
                
                

            Returns:
                Matplot Chart object
        """

         # Convert dataframe to a list of tuples for code to run.
        dt = list(df[[category_column, category_value_column, target_value_column]].itertuples(index=False, name=None))

        # Determine the max value for adjusting the bar height
        h = limits[-1] / 10

        # Use the 
        palette = sns.light_palette(palette_color, len(limits), reverse=False)

        # Must be able to handle one or many data sets via multiple subplots
        if len(dt) == 1:
            fig, ax = plt.subplots(figsize=size, sharex=True)
        else:
            fig, axarr = plt.subplots(len(dt), figsize=size, sharex=True)

        # Add each bullet graph bar to a subplot
        for idx, item in enumerate(dt):

            # Get the axis from the array of axes returned when the plot is created
            if len(dt) > 1:
                ax = axarr[idx]

            # Formatting to get rid of extra marking clutter
            ax.set_aspect('equal')
            ax.set_yticklabels([item[0]])
            ax.set_yticks([1])
            ax.spines['bottom'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

            prev_limit = 0
            for idx2, lim in enumerate(limits):
                # Draw the bar
                ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
                        color=palette[idx2])
                prev_limit = lim
            rects = ax.patches
            # The last item in the list is the value we're measuring
            # Draw the value we're measuring
            ax.barh([1], item[1], height=(h / 3), color=bar_color)

            # Need the ymin and max in order to make sure the target marker
            # fits
            ymin, ymax = ax.get_ylim()
            ax.vlines(
                item[2], ymin * .9, ymax * .9, linewidth=1.5, color=target_color)

        # Now make some labels
        if labels is not None:
            for rect, label in zip(rects, labels):
                height = rect.get_height()
                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    -height * .4,
                    label,
                    ha='center',
                    va='bottom',
                    color=label_color)
        if formatter:
            ax.xaxis.set_major_formatter(formatter)
        if axis_label:
            ax.set_xlabel(axis_label)
        if title:
            fig.suptitle(title, fontsize=14)
        g = fig.subplots_adjust(hspace=0)

        return g

@pf.register_dataframe_method
def funnel_graph(
    df,
    x_axis_column: str, 
    label_column: str,
    title: str ='Funnel Chart',
    xmin: int=0,
    xmax: int=100,  
    bar_color: str ='#808B96', 
    text_color: str ='#2A2A2A', 
    fill_color: str='grey'
    ):
    
    """Create bullet chart based on dataframe values.

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import charter
                >>> df.funnel_graph(
                ... x_axis_column = 'value1', 
                ... label_column='category', 
                ... title = 'Chart Title Here'
                ... )  # doctest: +SKIP


            Args:
                df: dataframe containing chart data
                x_axis_column: Column name of the x axis
                label_column: Column name of the labels
                title: Chart title
                xmin: x axis minimum. Default is 0.
                xmax: x axis maximum. Default is 100.
                bar_color: Bar color
                text_color: Text color
                fill_color: Fill color
                
            Returns:
                Matplot Chart object
    """

    x_list = df[x_axis_column].values.tolist()
    y = [*range(1, len(x_list)+1)]
    y.reverse()

    labels = df[label_column].values.tolist()
    x_range = xmax - xmin

    fig, ax = plt.subplots(1, figsize=(12,6))
    for idx, val in enumerate(x_list):
        left = (x_range - val)/2
        plt.barh(y[idx], x_list[idx], left = left, color=bar_color, height=.8)
        # label
        plt.text(50, y[idx]+0.1, labels[idx], ha='center', fontsize=16, color=text_color)
        # value
        plt.text(50, y[idx]-0.3, x_list[idx], ha='center', fontsize=16, color=text_color)
            
        if idx != len(x_list)-1:
            next_left = (x_range - x_list[idx+1])/2
            shadow_x = [left, next_left, 100-next_left, 100-left, left]
                
            shadow_y = [y[idx]-0.4, y[idx+1]+0.4, y[idx+1]+0.4, y[idx]-0.4, y[idx]-0.4]
            plt.fill(shadow_x, shadow_y, color=fill_color, alpha=0.6)
        plt.xlim(xmin, xmax)
        plt.axis('off')
        plt.title(title, loc='center', fontsize=24, color=text_color)
        plt.show()

@pf.register_dataframe_method
def dot_plot(df, sort_column, x_axis_column, y_axis_column, x_label, y_label, column_titles, xlim=(0, 25)):
    sns.set_theme(style='whitegrid')

    g = sns.PairGrid(
        df.sort_values(sort_column, ascending=False), 
        x_vars = df[x_axis_column],
        y_vars=df[y_axis_column],
        height=10,
        aspect=.25
    )

    g.map(sns.stripplot, size=10, orient='h', jitter=False, palette='flare_r', linewidth=1, edgecolor='w')
    g.set(xlim=xlim, xlabel=x_label, ylabel=y_label)

    for ax, title in zip(g.axes.flat, column_titles):
        # Sets title for each axes
        ax.set(title=title)
        # horizontal grid
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)
    
    sns.despine(left=True, bottom=True)

    return g

@pf.register_dataframe_method
def heatmap(
    df: pd.DataFrame,
      index_column: str, 
      columns: str,  
      values_columns: str 
    ):

    df = df.pivot(index=index_column, columns=columns, values=values_columns)
    #Draw heatmap with numeric values in each cell
    f, ax = plt.subplots(figsize=(9,6))
    hm = sns.heatmap(df, annot=True, fmt='d', linewidth=.5, ax=ax)

    return hm

@pf.register_dataframe_method
def multi_timeseries(
    df: pd.DataFrame, 
    x_axis_column: str, 
    y_axis_column: str, 
    hue: str, 
    facet_column: str = None, 
    x_label: str = '', 
    y_label: str = ''
):

    g = sns.relplot(
        data = df,
        x = x_axis_column,
        y = y_axis_column,
        col = facet_column,
        hue = hue,
        kind = 'line', 
        palette = 'crest',
        linewidth = 4,
        zorder = 5,
        col_wrap = 3,
        height = 2,
        aspect = 1.5,
        legend = False
    )

    for hue, ax in g.axes_dict.items():
            
        ax.text(.8, .85, hue, transform = ax.transAxes, fontweight='bold')

        sns.lineplot(
            data=df, 
            x=x_axis_column, 
            y=y_axis_column, 
            units=hue, 
            estimator=None, 
            color=".7", 
            linewidth=1, 
            ax=ax,
        )
        
    ax.set_xticks(ax.get_xticks()[::2])
    g.set_titles("")
    g.set_axis_labels(x_label, y_label)
    g.tight_layout()
    
    return g
