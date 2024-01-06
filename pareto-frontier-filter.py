import pandas as pd
import numpy as np

# Function to determine if points are Pareto efficient
def is_pareto_efficient(costs):
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    return is_efficient

# Load the data
data = pd.read_csv('/Users/jamesli/Documents/Projects/Misc./mk8d-build-stats/all-build-stats.csv')

# Select the stats for the Pareto Frontier calculation (excluding non-stat columns)
stats_columns = [col for col in data.columns if col not in ['Character', 'Vehicle', 'Tire', 'Glider']]
costs = data[stats_columns].values * -1  # Negating the values as we are dealing with costs
pareto_points = is_pareto_efficient(costs)

# Filter the data to only include Pareto efficient points
pareto_frontier_data = data.iloc[pareto_points]

# Save the Pareto efficient data to a new CSV file
pareto_frontier_data.to_csv('/Users/jamesli/Documents/Projects/Misc./mk8d-build-stats/pareto-frontier-builds.csv', index=False)
