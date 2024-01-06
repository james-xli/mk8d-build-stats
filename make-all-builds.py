import pandas as pd
from itertools import product

# Function to load and parse a CSV file
def load_csv(file_name):
    return pd.read_csv(file_name, index_col=0)

# Load each CSV file
characters = load_csv('characters.csv')
vehicles = load_csv('vehicles.csv')
tires = load_csv('tires.csv')
gliders = load_csv('gliders.csv')

# Prepare for combining the stats
combined_stats = []

# Iterate over all possible combinations
for char, veh, tire, glide in product(characters.index, vehicles.index, tires.index, gliders.index):
    combined_stat = characters.loc[char] + vehicles.loc[veh] + tires.loc[tire] + gliders.loc[glide]
    combined_stats.append([char, veh, tire, glide, *combined_stat.values])

# Create a DataFrame from the combined stats
combined_df = pd.DataFrame(combined_stats, columns=["Character", "Vehicle", "Tire", "Glider", *characters.columns])

# Save to a new CSV file
combined_df.to_csv('all-build-stats.csv', index=False)
