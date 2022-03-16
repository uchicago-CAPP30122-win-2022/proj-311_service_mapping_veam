'''
Graph: Map 2 (311 sevice requests)

311 Service Mapping Project

Create layout for second map (based on Chicago 311 service request data)
'''


# -----------------------------------------------------------
# Import statements
# !!!!!! QUESTION: NOT SURE WHAT WE DO OR DO NOT NEED

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# TO DELETE
# import pandas as pd
# import geopandas as gpd
# import numpy as np

from webapp.inputs.dicts import *
from webapp.inputs.data import df_311_census, geojson
from maindash import app # ACTION: this can be deleted when transferred to __main__


# -----------------------------------------------------------
# Layout - Core Components + Graph

resolution_times_graph = [
        html.Br(),
        dbc.Row(html.H3("Filter: Neighborhood 311 Service Request Statistics"),
                style={'text-align': 'center'},
                justify='center'),
        html.Br(),
        html.Br(),
        dbc.Row(
            dcc.Dropdown(id="311_map_filter",
                        options = [{'label': v, 'value':k} 
                                   for k, v in map_311_filter.items()],
                        multi = False,
                        value = "median_resol_time",
                        style = dropdown_style_d
                        ),
                justify='center'
                ),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(
            dcc.Graph(id='311_map', figure={'layout': {'paper_bgcolor': "#0f2537",
                                                        'plot_bgcolor': "#0f2537"}}, 
                       style = {'display': 'inline-block', 'width': '80vh', 'height': '80vh'}),
            justify='center'
        )
    ]


# -----------------------------------------------------------
# App Callback

# Update 311 map
@app.callback(
    Output(component_id = '311_map', component_property='figure'),
    [Input(component_id = '311_map_filter', component_property='value')]
    )

def update_311_map(filter_for_311):
    '''
    Updates 311 graph based on demo selected
    '''

    # Set the actual reference column
    map_output = df_311_census.copy()
    if filter_for_311 == "sr_per_1000":
        output_title = 'Avg. Annual Req. per 1k'
        colorbar_title = 'Req./1k'
    else:
        output_title = 'Days' 
        colorbar_title = output_title

    map_output[output_title] = map_output[filter_for_311]
    map_output[colorbar_title] = map_output[filter_for_311]

    # Set color bounds
    max_val = map_output[output_title].max()
    max_str = str(int(max_val))
    num_zero = len(max_str) - 1
    first_digit = max_str[0]
    first_digit = str(int(first_digit) + 1)
    max_val = int(first_digit + "0" * num_zero)

    # Specify map figure
    fig = px.choropleth_mapbox(
        data_frame=map_output,
        geojson=geojson,
        color=colorbar_title,
        color_continuous_scale='blues',
        locations="cca_num_x",
        zoom=9, 
        center = {"lat": 41.8, "lon": -87.75},
        opacity=0.8,
        featureidkey="properties.area_numbe",
        mapbox_style="open-street-map",
        hover_name="cca_name",
        range_color=[0, max_val],
        hover_data={output_title: True,
                    'Top 311 issue': True,
                    '2nd issue': True,
                    '3rd issue': True,
                    'cca_num_x': False},
        title=f"{map_311_filter[filter_for_311]}"
        )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(paper_bgcolor="#0f2537", font_color = '#fff')  

    return fig