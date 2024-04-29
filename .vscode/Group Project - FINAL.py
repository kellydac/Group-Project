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
    
    # Filter batting data for players with over 100 AB
    batting_df = batting_df[batting_df['AB'] > 100]
    
    # Filter pitching data for players with over 150 IPouts and more than zero ERA
    pitching_df = pitching_df[(pitching_df['IPouts'] > 150) & (pitching_df['ERA'] > 0)]
    
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
    # Define age categories from 20 to 40 years old
    bins = [20, 23, 26, 29, 32, 35, 38, 41]
    labels = ['20-22', '23-25', '26-28', '29-31', '32-34', '35-37', '38-40']
    
    # Categorize age using cut function
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    
    return df

# Define function to calculate batting average
def calculate_batting_average(df):
    # Calculate batting average
    df['batting_avg'] = df['H'] / df['AB']
    df['batting_avg'] = df['batting_avg'].fillna(0)  # Fill NaN values with 0
    
    return df

# Define function to calculate BB/K ratio for batting data
def calculate_bb_k_ratio(df):
    # Calculate BB/K ratio
    df['bb_k_ratio'] = df['BB'] / df['SO']
    df['bb_k_ratio'] = df['bb_k_ratio'].fillna(0)  # Fill NaN values with 0
    
    return df

# Define function to calculate K/BB ratio for pitching data
def calculate_k_bb_ratio(df):
    # Calculate K/BB ratio
    df['k_bb_ratio'] = df['SO'] / df['BB']
    df['k_bb_ratio'] = df['k_bb_ratio'].fillna(0)  # Fill NaN values with 0
    
    return df

# Define function to calculate summary statistics for performance metrics
def calculate_summary_statistics(df, performance_metrics):
    # Filter data where performance metric is greater than 0
    df = df[df[performance_metrics] > 0]
    
    # Group data by age group and calculate median and standard deviation of performance metrics
    summary_stats = df.groupby('age_group')[performance_metrics].agg(['median', 'std']).reset_index()
    
    print(f"Summary Statistics Dataframe for {performance_metrics}:")
    print(summary_stats)  # Print first few rows of summary statistics dataframe
    
    # Find age range representing peak performance
    if performance_metrics in ['ERA', 'BAOpp']:
        peak_age_group = summary_stats.loc[summary_stats['median'].idxmin(), 'age_group']
    else:
        peak_age_group = summary_stats.loc[summary_stats['median'].idxmax(), 'age_group']
    print(f"Peak Performance Age Range for {performance_metrics}: {peak_age_group} years old.")
    print(' ')
    
    return summary_stats

# Define function to plot line graph for performance metrics by age category
def plot_performance_by_age(summary_stats, performance_metric):
    # Plot line graph for performance metric by age category
    plt.figure(figsize=(10, 6))
    plt.plot(summary_stats['age_group'], summary_stats['median'], marker='o', label='Median', color='blue')
    plt.fill_between(summary_stats['age_group'], summary_stats['median'] - summary_stats['std'], summary_stats['median'] + summary_stats['std'], alpha=0.2)
    plt.xlabel('Age Group (years)')
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
    
    # Calculate player age for batting and pitching data
    batting_df = calculate_age(batting_df)
    pitching_df = calculate_age(pitching_df)
    
    # Categorize player age into age groups
    batting_df = categorize_age(batting_df)
    pitching_df = categorize_age(pitching_df)
    
    # Calculate batting average
    batting_df = calculate_batting_average(batting_df)
    
    # Calculate BB/K ratio for batting data
    batting_df = calculate_bb_k_ratio(batting_df)
    
    # Calculate K/BB ratio for pitching data
    pitching_df = calculate_k_bb_ratio(pitching_df)
    
    # List of performance metrics to analyze
    batting_performance_metrics = {'Home Runs': 'HR', 'Batting Average': 'batting_avg', 'BB/K Ratio': 'bb_k_ratio'}
    pitching_performance_metrics = {'Earned Run Average': 'ERA', 'Innings Pitched': 'IPouts', 'Strikeouts': 'SO', 'Opponent Batting Average': 'BAOpp', 'K/BB Ratio': 'k_bb_ratio'}
    
    # Analyze each performance metric for batting
    for metric_name, metric_abbr in batting_performance_metrics.items():
        # Calculate summary statistics for the metric by age group for batting
        batting_summary_stats = calculate_summary_statistics(batting_df, metric_abbr)
        
        # Plot line graph for the metric by age group for batting
        plot_performance_by_age(batting_summary_stats, metric_name)
    
    # Analyze each performance metric for pitching
    for metric_name, metric_abbr in pitching_performance_metrics.items():
        # Calculate summary statistics for the metric by age group for pitching
        pitching_summary_stats = calculate_summary_statistics(pitching_df, metric_abbr)
        
        # Plot line graph for the metric by age group for pitching
        plot_performance_by_age(pitching_summary_stats, metric_name)

if __name__ == "__main__":
    main()