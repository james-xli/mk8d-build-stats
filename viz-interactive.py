import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv('/Users/jamesli/Documents/Projects/Misc./mk8d-build-stats/all-build-stats-simplified.csv')

# Function to determine if points are Pareto efficient
def is_pareto_efficient(costs):
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    return is_efficient

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[{'label': col, 'value': col} for col in data.columns if col not in ['Character', 'Vehicle', 'Tire', 'Glider']],
        value='Speed_Avg'
    ),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[{'label': col, 'value': col} for col in data.columns if col not in ['Character', 'Vehicle', 'Tire', 'Glider']],
        value='Handling_Avg'
    ),
    dcc.Dropdown(
        id='z-axis-dropdown',
        options=[{'label': col, 'value': col} for col in data.columns if col not in ['Character', 'Vehicle', 'Tire', 'Glider']],
        value='Accel'
    ),
    dcc.Graph(id='pareto-plot')
])

# Callback to update the plot
@app.callback(
    Output('pareto-plot', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('z-axis-dropdown', 'value')]
)
def update_graph(x_stat, y_stat, z_stat):
    costs = data[[x_stat, y_stat, z_stat]].values * -1
    pareto_points = is_pareto_efficient(costs)

    # Creating a Plotly 3D scatter plot
    fig = go.Figure()

    # All points
    fig.add_trace(go.Scatter3d(x=data[x_stat], y=data[y_stat], z=data[z_stat],
                               mode='markers', name='All Points',
                               marker=dict(size=3, color='blue', opacity=0.3),
                               hoverinfo='text',
                               text=data[['Character', 'Vehicle', 'Tire', 'Glider']].agg(', '.join, axis=1)))

    # Pareto Frontier
    pareto_frontier_data = data.iloc[pareto_points]
    fig.add_trace(go.Scatter3d(x=pareto_frontier_data[x_stat], 
                               y=pareto_frontier_data[y_stat], 
                               z=pareto_frontier_data[z_stat],
                               mode='markers', name='Pareto Frontier',
                               marker=dict(size=5, color='red'),
                               hoverinfo='text',
                               text=pareto_frontier_data[['Character', 'Vehicle', 'Tire', 'Glider']].agg(', '.join, axis=1)))

    # Update the layout of the plot
    fig.update_layout(scene=dict(
                        xaxis_title=x_stat,
                        yaxis_title=y_stat,
                        zaxis_title=z_stat),
                      title='Pareto Frontier Plot in 3D',
                      height=800,  # Adjust height to fill more of the screen
                      margin=dict(l=10, r=10, b=10, t=30))  # Adjust margins as needed)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
