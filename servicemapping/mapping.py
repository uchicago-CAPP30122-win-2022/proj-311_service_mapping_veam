'''
App Layout

311 Service Mapping Project

Set overall app layout for 311 Service Mapping Project
'''


# -----------------------------------------------------------
# Import statements
# QUESTION/ACTION: CHECK WHAT WE DO OR DO NOT NEED TO KEEP

import dash
from dash import html
import dash_bootstrap_components as dbc

# TO DELETE
# from dash.dependencies import Input, Output
# from dash import dcc
# import plotly.express as px
# import pandas as pd
# import geopandas as gpd
# import numpy as np
# import statsmodels
# from data_pull.census.create_cca_tract_dict import create_dictionaries

from webapp.graphs.graph_map1 import *
from webapp.graphs.graph_map2 import *
from webapp.graphs.graph_bars import *
from webapp.graphs.graph_scatter import *
from maindash import app # ACTION: this can be deleted when transferred to __main__


# -----------------------------------------------------------
# App Layout

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
    dbc.Row("Sources: Chicago 311 Service Request Data (Chicago Data Portal) & American Community Survey (2019)"),
    dbc.Row(html.Br())
    ]
    ,fluid=True, style={'backgroundColor':'#0f2537'}
    )

# # ACTION: Do we put this in main, or leave here?
if __name__ == '__main__':
    app.run_server(debug=True)
