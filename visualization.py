import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load the data
data = pd.read_csv('/Users/jamesli/Documents/Projects/Misc./mk8d-build-stats/all-build-stats.csv')

# Function to determine if points are Pareto efficient
def is_pareto_efficient(costs):
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    return is_efficient

# Select the stats for the Pareto Frontier calculation
selected_stats = ['Speed_Land', 'Speed_Water', 'Accel']
costs = data[selected_stats].values * -1  # Negating the values as we are dealing with costs
pareto_points = is_pareto_efficient(costs)

# Creating a Plotly 3D scatter plot
fig = go.Figure()

# All points
fig.add_trace(go.Scatter3d(x=data[selected_stats[0]], y=data[selected_stats[1]], z=data[selected_stats[2]],
                           mode='markers', name='All Points',
                           marker=dict(size=3, color='blue', opacity=0.3),
                           hoverinfo='text',
                           text=data[['Character', 'Vehicle', 'Tire', 'Glider']].agg(', '.join, axis=1)))

# Pareto Frontier
pareto_frontier_data = data.iloc[pareto_points]
fig.add_trace(go.Scatter3d(x=pareto_frontier_data[selected_stats[0]], 
                           y=pareto_frontier_data[selected_stats[1]], 
                           z=pareto_frontier_data[selected_stats[2]],
                           mode='markers', name='Pareto Frontier',
                           marker=dict(size=5, color='red'),
                           hoverinfo='text',
                           text=pareto_frontier_data[['Character', 'Vehicle', 'Tire', 'Glider']].agg(', '.join, axis=1)))

# Update the layout of the plot
fig.update_layout(scene=dict(
                    xaxis_title=selected_stats[0],
                    yaxis_title=selected_stats[1],
                    zaxis_title=selected_stats[2]),
                  title='Pareto Frontier Plot in 3D')

# Display the plot
# fig.show()  # This will display the plot in an interactive window if run in a suitable environment

fig.write_html( 'output_file_name.html', 
                   auto_open=True )