# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('🚀 SpaceX Launch Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'All Sites'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                        ],
                                        placeholder='Select a Launch Site',
                                        value='All Sites',
                                        searchable=True,
                                        style={'width': '60%', 'margin': 'auto'}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.P("Payload range (kg):", style={'textAlign': 'center', 'fontSize': 18}),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=500,
                                                marks={i: str(i) for i in range(0, 10001, 2000)},
                                                value=[min_payload, max_payload],
                                                tooltip={"placement": "bottom", "always_visible": True}),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'All Sites':
        df_grouped = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = px.pie(df_grouped, values='class', names='Launch Site',
                     title="Success Rate by Launch Site",
                     color_discrete_sequence=px.colors.sequential.Blues)
    else:
        df_filtered = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(df_filtered, names='class', title=f"Success vs Failure at {selected_site}",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')])
def update_scatter_plot(selected_site, payload_range):
    filtered_df = spacex_df.loc[
        (spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1]))
    ]
    if selected_site != 'All Sites':
        filtered_df = filtered_df.loc[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                     color="Booster Version Category",
                     title=f"Payload vs Success Rate ({'All Sites' if selected_site == 'All Sites' else selected_site})",
                     hover_data=['Launch Site'],
                     color_discrete_sequence=px.colors.qualitative.Set1)
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
