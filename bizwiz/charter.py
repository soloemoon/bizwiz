class bizcharts:
    def __init__(self, data):
        self.data = data

    def bullet_graph(self, category_col, category_value_col, target_value_col, limits=None, labels=['Poor', 'Ok', 'Good', 'Excellent'], axis_label='Metric', title='Bullet Graph',
                size=(5, 3), palette_color='green', formatter=None, target_color="gray",
                bar_color="black", label_color="black"
                ):

        d = self.data[[category_col, category_value_col, target_value_col]].copy()

        # Convert dataframe to a list of tuples for code to run.
        dt = list(d.itertuples(index=False, name=None))
        del d
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
    
    def funnel_chart(self, x_col, label_col, title='', xmax=100, xmin=0, bar_color='#808B96', text_color='#2A2A2A', fill_color='grey'):
        """
        Creates a funnel chart.

        Parameters
        ----------
        limits : list
            List of range values to increment x axis by
        labels : list, optional
            List of shading description descriptions. Default is ['Poor', 'Ok', 'Good', 'Excellent']
        axis_label : str, optional
            The x axis label name. Default is metric
        title: str, optional
            Title of bullet graph. Default is 'Bullet Graph'
        size: tuple, optional
            Tuple for plot size. Default is (5,3)
        palette_color:s str, optional
            Seaborn color palette to be used. Default is green.
        formatter: object, optional
            Matplotlib formatter object for x axis
        target_color: str, optional
            Color of the target line. Default is grey
        bar_color: str, optional
            Color of the value bars. Default is black
        label_color: str, optional
            Color of the chart labels. Default is black.
        """

        x_list = self.data[x_col].values.tolist()
        y = [*range(1, len(x_list)+1)]
        y.reverse()

        labels = self.data[label_col].values.tolist()
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
                shadow_x = [left, next_left, 
                            100-next_left, 100-left, left]
                
                shadow_y = [y[idx]-0.4, y[idx+1]+0.4, 
                            y[idx+1]+0.4, y[idx]-0.4, y[idx]-0.4]
                plt.fill(shadow_x, shadow_y, color=fill_color, alpha=0.6)
        plt.xlim(xmin, xmax)
        plt.axis('off')
        plt.title(title, loc='center', fontsize=24, color=text_color)
        plt.show()

    def dot_plot(self, sort_column, x_columns, y_column, xlabel, ylabel, column_titles, xlim=(0,25)):
       
        # Data should be in individual columns with values in rows (wide)
        sns.set_theme(style="whitegrid")
        g = sns.PairGrid(self.data.sort_values(sort_column, ascending=False),
                 x_vars=self.data[x_columns], y_vars=[y_column],
                 height=10, aspect=.25)
        
        # Draw a dot plot using the stripplot function
        g.map(sns.stripplot, size=10, orient="h", jitter=False, palette="flare_r", linewidth=1, edgecolor="w")

        # Use the same x axis limits on all columns and add better labels
        g.set(xlim=xlim, xlabel=xlabel, ylabel=ylabel)

        for ax, title in zip(g.axes.flat, column_titles):

            # Set a different title for each axes
            ax.set(title=title)

            # Make the grid horizontal instead of vertical
            ax.xaxis.grid(False)
            ax.yaxis.grid(True)

        sns.despine(left=True, bottom=True)

        return g
    
    def barh(self, sort_column, total_x, second_x, y, total_label, second_label, bar_color, legend_location='lower right', xlim=(0, 24), ylabel='', xlabel=''):


        sns.set_theme(style="whitegrid")

        df = self.data.sort_values(sort_column, ascending=False)
        # Initialize the matplotlib figure
        f, ax = plt.subplots(figsize=(6, 15))

        # Plot the total
        sns.set_color_codes("pastel")
        sns.barplot(x=total_x, y=y, data=df,
                    label=total_label, color=bar_color)

        # Plot the crashes where alcohol was involved
        sns.set_color_codes("muted")
        sns.barplot(x=second_x, y=y, data=df,
                    label=second_label, color=bar_color)

        # Add a legend and informative axis label
        ax.legend(ncol=2, loc=legend_location, frameon=True)
        ax.set(xlim=xlim, ylabel=ylabel,
            xlabel=xlabel)
        sns.despine(left=True, bottom=True)
    
    def heatmap(self, index, columns, values):
        df = self.data.pivot(index=index, columns=columns, values=values)
        # Draw a heatmap with the numeric values in each cell
        f, ax = plt.subplots(figsize=(9, 6))
        sns.heatmap(df, annot=True, fmt="d", linewidths=.5, ax=ax)

    def multi_timeseries(self, x, y, column, hue, xlabel='', ylabel='' ):
        g = sns.relplot(
            data = self.data,
            x = x,
            y =y,
            col = column,
            hue = hue,
            kind= 'line', palette='crest', linewidth=4, zorder=5,
                col_wrap=3, height=2, aspect=1.5, legend=False, 
                    )

        for hue, ax in g.axes_dict.items():
            ax.text(.8, .85, hue, transform = ax.transAxes, fontweight='bold')

            sns.lineplot(
                data=self.data, x=x, y=y, units=hue, estimator=None, color=".7", linewidth=1, ax=ax,
            )
        
        ax.set_xticks(ax.get_xticks()[::2])
        g.set_titles("")
        g.set_axis_labels(xlabel, ylabel)
        g.tight_layout()
        return g
    
    
    