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
    # Define age categories from 20 to 38 years old
    bins = [20, 24, 28, 32, 36, 40]
    labels = ['20-24', '25-28', '29-32', '33-36', '37-40']
    
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
    print(summary_stats)
    print()  # Empty line for readability
    
    return summary_stats

# Define function to plot line graph for performance metrics by age category
def plot_performance_by_age(summary_stats, performance_metric):
    # Plot line graph for performance metric by age category
    plt.figure(figsize=(10, 6))
    plt.plot(summary_stats['age_group'], summary_stats[f'{performance_metric}_mean'], marker='o', label='Mean', color='red')
    plt.fill_between(summary_stats['age_group'], summary_stats[f'{performance_metric}_mean'] - summary_stats[f'{performance_metric}_std'], summary_stats[f'{performance_metric}_mean'] + summary_stats[f'{performance_metric}_std'], alpha=0.2)
    plt.xlabel('Age Group')
    plt.ylabel(performance_metric)
    plt.title(f'{performance_metric} by Age Group')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.ylim(bottom=0)  # Start the y-axis from 0
    plt.tight_layout()
    plt.show()

# Main function to execute the analysis
def main():
    # Merge data from spreadsheets
    batting_df, pitching_df = merge_data(folder_path)
    
    # Calculate player age for batting and pitching data
    batting_df = calculate_age(batting_df)
    pitching_df = calculate_age(pitching_df)
    
    # Filter data based on age and performance criteria
    batting_df = batting_df[(batting_df['age'] >= 20) & (batting_df['age'] <= 38) & (batting_df['AB'] > 0)]
    pitching_df = pitching_df[(pitching_df['age'] >= 20) & (pitching_df['age'] <= 38) & (pitching_df['IPouts'] > 0) & (pitching_df['ERA'] != 0)]
    
    # Categorize player age into age groups
    batting_df = categorize_age(batting_df)
    pitching_df = categorize_age(pitching_df)
    
    # Calculate batting average for batting data
    batting_df = calculate_batting_average(batting_df)
    
    # List of performance metrics to analyze
    batting_performance_metrics = ['HR', 'AB', 'SO', 'batting_avg']
    pitching_performance_metrics = ['ERA', 'IPouts']
    
    # Calculate summary statistics for batting performance metrics
    print("Batting Summary Statistics:")
    batting_summary_stats = calculate_summary_statistics(batting_df, batting_performance_metrics)
    
    # Plot line graph for batting performance metrics by age category
    for metric in batting_performance_metrics:
        plot_performance_by_age(batting_summary_stats, metric)
    
    # Calculate summary statistics for pitching performance metrics
    print("Pitching Summary Statistics:")
    pitching_summary_stats = calculate_summary_statistics(pitching_df, pitching_performance_metrics)
    
    # Plot line graph for pitching performance metrics by age category
    for metric in pitching_performance_metrics:
        plot_performance_by_age(pitching_summary_stats, metric)

if __name__ == "__main__":
    main()
