import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the directory where the spreadsheets are located
folder_path = r'C:\Users\DacanayKC20\Downloads'

# Define function to read and merge data
def merge_data(folder_path):
    # Read the People.xlsx, Batting.xlsx, and Pitching.xlsx files
    people_df = pd.read_excel(os.path.join(folder_path, 'People.xlsx'))
    batting_df = pd.read_excel(os.path.join(folder_path, 'Batting.xlsx'))
    pitching_df = pd.read_excel(os.path.join(folder_path, 'Pitching.xlsx'))
    
    # Merge People dataframe with Batting and Pitching dataframes using playerID as the key
    merged_batting_df = pd.merge(people_df, batting_df, on='playerID', how='inner')
    merged_pitching_df = pd.merge(people_df, pitching_df, on='playerID', how='inner')
    
    return merged_batting_df, merged_pitching_df

# Define function to calculate player age at each performance record
def calculate_age(df):
    # Convert yearID and birthYear to datetime objects for calculation
    df['yearID'] = pd.to_datetime(df['yearID'], format='%Y')
    df['birthYear'] = pd.to_datetime(df['birthYear'], format='%Y')
    
    # Calculate player age by subtracting birthYear from yearID and convert to years
    df['age'] = (df['yearID'] - df['birthYear']).dt.days // 365
    
    return df

# Define function to group players into age categories
def categorize_age(df):
    # Define age categories from 18 to 49 years old
    bins = [18, 24, 29, 34, 39, 44, 49]
    labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49']
    
    # Categorize age using cut function
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    
    return df

# Define function to calculate batting average
def calculate_batting_average(df):
    # Calculate batting average
    df['batting_avg'] = df['H'] / df['AB']
    df['batting_avg'] = df['batting_avg'].fillna(0)  # Fill NaN values with 0
    
    return df

# Define function to calculate summary statistics for performance metrics
def calculate_summary_statistics(df, performance_metrics):
    # Group data by age group and calculate mean, median, and standard deviation of performance metrics
    summary_stats = df.groupby('age_group')[performance_metrics].agg(['mean', 'median', 'std']).reset_index()
    
    print("Summary Statistics Dataframe:")
    print(summary_stats.head())  # Print first few rows of summary statistics dataframe
    
    return summary_stats

# Define function to plot line graph for performance metrics by age category
def plot_performance_by_age(summary_stats, performance_metric):
    # Plot line graph for performance metric by age category
    plt.figure(figsize=(10, 6))
    plt.plot(summary_stats['age_group'], summary_stats['mean'], marker='o', label='Mean')
    plt.plot(summary_stats['age_group'], summary_stats['median'], marker='o', label='Median')
    plt.fill_between(summary_stats['age_group'], summary_stats['mean'] - summary_stats['std'], summary_stats['mean'] + summary_stats['std'], alpha=0.2)
    plt.xlabel('Age Group')
    plt.ylabel(performance_metric)
    plt.title(f'{performance_metric} by Age Group')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main function to execute the analysis
def main():
    # Merge data from spreadsheets
    batting_df, pitching_df = merge_data(folder_path)
    
    # Print column names of batting and pitching dataframes
    print("Batting Dataframe Columns:", batting_df.columns)
    print("Pitching Dataframe Columns:", pitching_df.columns)
    
    # Calculate actual player ages for batting and pitching data
    batting_df = calculate_age(batting_df)
    pitching_df = calculate_age(pitching_df)
    
    # Group players into age categories
    batting_df = categorize_age(batting_df)
    pitching_df = categorize_age(pitching_df)
    
    # Calculate batting average for each age group
    batting_df = calculate_batting_average(batting_df)
    
    # Define the most important performance metrics for batting and pitching
    batting_performance_metrics = ['HR', 'AB', 'SO', 'batting_avg']
    pitching_performance_metrics = ['ERA', 'IPouts']
    
    # Analyze each performance metric for batting
    for metric in batting_performance_metrics:
        try:
            # Calculate summary statistics for the metric by age group for batting
            batting_summary_stats = calculate_summary_statistics(batting_df, [metric])
            
            # Plot line graph for the metric by age group for batting
            plot_performance_by_age(batting_summary_stats, metric)
        except KeyError as e:
            print(f"Error occurred for metric '{metric}': {e}")

    # Analyze each performance metric for pitching
    for metric in pitching_performance_metrics:
        try:
            # Calculate summary statistics for the metric by age group for pitching
            pitching_summary_stats = calculate_summary_statistics(pitching_df, [metric])
            
            # Plot line graph for the metric by age group for pitching
            plot_performance_by_age(pitching_summary_stats, metric)
        except KeyError as e:
            print(f"Error occurred for metric '{metric}': {e}")

if __name__ == "__main__":
    main()
