import pandas as pd

# Define file paths for the spreadsheets
people_path = r'C:\Users\DacanayKC20\Downloads\People.xlsx'
batting_path = r'C:\Users\DacanayKC20\Downloads\Batting.xlsx'
pitching_path = r'C:\Users\DacanayKC20\Downloads\Pitching.xlsx'

# Read data from the spreadsheets
people_data = pd.read_excel(people_path)
batting_data = pd.read_excel(batting_path)
pitching_data = pd.read_excel(pitching_path)

# Extract relevant columns from each spreadsheet
people_birth_years = people_data['birthYear']  # Extract birthYear column from People.xlsx

batting_hr = batting_data['HR']  # Extract HR column from Batting.xlsx
batting_hits = batting_data['H']  # Extract H column from Batting.xlsx
batting_sb = batting_data['SB']  # Extract SB column from Batting.xlsx

pitching_era = pitching_data['ERA']  # Extract ERA column from Pitching.xlsx
pitching_strikeouts = pitching_data['SO']  # Extract SO column from Pitching.xlsx

# Perform statistical analysis on the extracted data
# Here, you can calculate mean, median, standard deviation, or any other desired statistics
# For brevity, let's calculate the mean for each category
mean_hr = batting_hr.mean()
mean_hits = batting_hits.mean()
mean_sb = batting_sb.mean()

mean_era = pitching_era.mean()
mean_strikeouts = pitching_strikeouts.mean()

# Print out the results
print("Statistical Analysis Results:")
print("Batting Statistics:")
print(" - Mean Home Runs (HR):", mean_hr)
print(" - Mean Hits (H):", mean_hits)
print(" - Mean Stolen Bases (SB):", mean_sb)
print("\nPitching Statistics:")
print(" - Mean Earned Run Average (ERA):", mean_era)
print(" - Mean Strikeouts (SO):", mean_strikeouts)
