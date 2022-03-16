'''
App Layout

311 Service Mapping Project

Set overall app layout for 311 Service Mapping Project
'''

import dash
from dash import html
import dash_bootstrap_components as dbc
from servicemapping.webapp.graphs.graph_map1 import demo_map
from servicemapping.webapp.graphs.graph_map2 import resolution_times_graph
from servicemapping.webapp.graphs.graph_bars import middle_row_content
from servicemapping.webapp.graphs.graph_scatter import bottom_row_content
from servicemapping.maindash import app


# -----------------------------------------------------------
# App Layout

source_note = "Sources: Chicago 311 Service Request Data (Chicago Data Portal)\
               & American Community Survey (2019)"

app.layout = dbc.Container([
    html.Br(),
    dbc.Row(
        html.H1("How Neighborhood Demographics Impact 311 Responsiveness",
                style={'text-align': 'center'}), justify='center'),
    dbc.Row([dbc.Col(demo_map), dbc.Col(resolution_times_graph)]),
    html.Br(),
    dbc.Row(middle_row_content),
    html.Br(),
    dbc.Row(bottom_row_content),
    dbc.Row(source_note),
    dbc.Row(html.Br())
    ]
    ,fluid=True, style={'backgroundColor':'#0f2537'}
    )

if __name__ == '__main__':
    app.run_server(debug=True)
