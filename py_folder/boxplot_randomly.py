__author__ = 'Zhipeng He'

#imports
import pandas as pd
from parsers.processing_data import *
import seaborn as sns
import matplotlib.pyplot as plt


def select_random_days(data_frame, start_date, end_date, days):
    # Convert start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date) 
    # Filter the DataFrame to include only the desired time period
    filtered_df = data_frame[(data_frame['Date'] >= start_date) & (data_frame['Date'] <= end_date)]   
    # Randomly sample n dates
    random_dates = filtered_df['Date'].sample(n=days, replace=False, random_state=42)  
    return random_dates

def render_boxplot(df, id='2', variable='Fiber'):
    # Select the data from the dataframe
    df = df.loc[df['ID'] == id]
    
    # Define the baseline and control periods
    if id == 1:
        baseline_dates = pd.date_range(start='2024-01-29', periods=8)
        control_dates = select_random_days(df, '2024-02-14', '2024-03-18', 8)
    else:
        baseline_dates = pd.date_range(start='2024-01-08', periods=14)
        control_dates = select_random_days(df, '2024-01-22', '2024-03-05', 14)
 
    # Filter data for baseline and control periods
    baseline_data = df[df['Date'].isin(baseline_dates)]
    control_data = df[df['Date'].isin(control_dates)]

    # Prepare data for box plot
    data = pd.concat([baseline_data[variable], control_data[variable]], axis=1)
    data.columns = ['Baseline', 'Control']

    # Create boxplot using Seaborn
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, palette="Set3")
    plt.title(f"Boxplot of person_{id}'s {variable}")
    plt.xlabel('Groups')
    plt.ylabel(variable)
    plt.tight_layout()

    name = f"'Person_'{id}_{variable}.png"
    plt.savefig(name)
    plt.show()


# To test if this works
def main():
    df, _ = data_processing() # _ lt lays a df_raw that was not interpolated by linear method
    plot = render_boxplot(df, id=2, variable='Systolic blood pressure (evening)')  # id = 1,2,3,4 or 5
    
    
if __name__ == "__main__":
    main()








