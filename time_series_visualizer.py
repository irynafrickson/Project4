import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 0, parse_dates = True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
 
    df_line = df.copy()
    df_line.reset_index(inplace=True)
 
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))

    ax.plot(df_line['date'], df_line['value'], linestyle = 'solid')

    # Customize the plot
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():

    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)

    # Ensure the 'date' column is in datetime format
    df_bar['date'] = pd.to_datetime(df_bar['date'])
    
    # Extract year and month from the date
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.strftime('%B')  # Month name
    
    # Group by year and month, calculate average daily views
    grouped = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
    
    # Get unique years and months
    years = sorted(grouped['year'].unique())
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Prepare data for plotting
    bar_width = 0.8 / len(months)  # Width of each bar, adjusted for number of months
    x = np.arange(len(years))  # Positions for years
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw bar plot
    # Plot bars for each month
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78']   # Distinct colors for 12 months

    for i, month in enumerate(months):
        # Get data for the current month across all years
        month_data = grouped[grouped['month'] == month]
        # Ensure data for all years, fill with 0 if no data
        data = [month_data[month_data['year'] == year]['value'].iloc[0] if year in month_data['year'].values else 0 for year in years]
        # Plot bars, offset by month index
        ax.bar(x + i * bar_width - (bar_width * (len(months) - 1) / 2), data, bar_width, label=month, color=colors[i])
    
    # Customize the plot
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Page Views by Month and Year')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(title='Months')

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Draw box plots (using Seaborn)

    # Create a figure with two subplots side by side
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Boxplots by Years
    sns.boxplot(x="year", y="value", data=df_box, palette='Set1', hue='year', legend=False, ax=axes[0])
    axes[0].set(title="Year-wise Box Plot (Trend)", xlabel = 'Year', ylabel = 'Page Views')
    
    # Plot 2: Boxplots by Month
    sns.boxplot(x="month", y="value", data=df_box, palette='Set2', hue='month', legend=False, order = months, ax=axes[1])
    axes[1].set(title="Month-wise Box Plot (Seasonality)", xlabel='Month', ylabel = 'Page Views')

    # Adjust layout for better spacing
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
