'''
A file to create our website in plotly
'''
# LIST OF THINGS LATER?
# do color scheme 0 to max(percent of category) instead of 0-100
# add filter for other categories (subfilters)
# connect 311 data to 2nd graph
# fix hover labels (show percentages instead of ratio)
# replicate with scatterplot and bar plot (on the bottom)
# add headers for the graphs
# slightly adjust graph sizes
# font/color

# LINKS
# https://plotly.com/python/setting-graph-size/
# https://dash.plotly.com/basic-callbacks
# https://dash.plotly.com/dash-core-components/dropdown

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd

# https://plotly.com/python/choropleth-maps/
# https://www.youtube.com/watch?v=hSPmj7mK6ng&list=TLPQMDIwMzIwMjK-RX-K6Ja5bw&index=5

app = dash.Dash(__name__)

# -----------------------------------------------------------
# Import and clean data
census_data = pd.read_csv("data/census_demos.csv")
census_data["cca_num"] = census_data["cca_num"].astype(str)
geojson = gpd.read_file("data/community_areas.geojson")

# -----------------------------------------------------------
# App layout

app.layout = dbc.Container([
    dbc.Row(dbc.Col(
        html.H1("How demographics impact 311 data", style={'text-align': 'center'}))#,
    ),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="select_race",
                        options =[
                            {"label": "White", "value": "White"},
                            {"label": "Black", "value": "Black_or_African_American"},
                            {"label": "Native American", "value": "American_Indian_or_Alaska_Native"},
                            {"label": "Asian", "value": "Asian"},
                            {"label": "Native_Hawaiian_or_Other_Pacific_Islander", "value": "Native_Hawaiian_or_Other_Pacific_Islander"},
                            {"label": "Other single race", "value": "some_other_race_alone"},
                            {"label": "2+ races", "value": "two_or_more_races"}],
                        multi = False,
                        value = "White",
                        style = {'width': '40%', 'display': 'inline-block', 'text-align': 'center'}
                        ),

            # Graph 1 duplicate
            dcc.Dropdown(id="select_race2",
                        options =[
                            {"label": "White", "value": "White"},
                            {"label": "Black", "value": "Black_or_African_American"},
                            {"label": "Native American", "value": "American_Indian_or_Alaska_Native"},
                            {"label": "Asian", "value": "Asian"},
                            {"label": "Native_Hawaiian_or_Other_Pacific_Islander", "value": "Native_Hawaiian_or_Other_Pacific_Islander"},
                            {"label": "Other single race", "value": "some_other_race_alone"},
                            {"label": "2+ races", "value": "two_or_more_races"}],
                        multi = False,
                        value = "White",
                        style = {'width': '40%', 'display': 'inline-block', 'text-align': 'center'}
                        )

            ])

        ]),

    dbc.Row([
        dbc.Col([

            dcc.Graph(id='demo_map', figure={}, style = {'display': 'inline-block'}),
            dcc.Graph(id='demo_map2', figure={}, style = {'display': 'inline-block'})
            
            ])

        ])

    ], fluid=True)

# -----------------------------------------------------------
# Connect the Plotly graphs with Dash Componenets
@app.callback(
    [Output(component_id = 'demo_map', component_property='figure'),
    Output(component_id = 'demo_map2', component_property='figure')],

    [Input(component_id = 'select_race', component_property='value'),
    Input(component_id = 'select_race2', component_property='value')]
    )

def update_graph(race, race2):
    '''
    Updates graph based on race selected
    '''
    fig = px.choropleth(
        data_frame=census_data,
        geojson=geojson,
        color=race,
        locations="cca_num",
        featureidkey="properties.area_numbe",
        projection="mercator",
        hover_name="cca_name",
        hover_data=[race],
        range_color=[0,100],
        title=f"% {race} by Chicago Neighobrhood (ACS 2019)"
        # width=400,
        # height=800
        )

    fig2 = px.choropleth(
        data_frame=census_data,
        geojson=geojson,
        color=race2,
        locations="cca_num",
        featureidkey="properties.area_numbe",
        projection="mercator", 
        range_color=[0,100],
        hover_name="cca_name",
        hover_data=[race2],
        title=f"% {race2} by Chicago Neighborhood (Chicago 311 Requests)"
        # width=400,
        # height=800
        )

    fig.update_geos(fitbounds='locations', visible=False)
    # fig.update_traces(hoverinfo='location+cca_name')
    
    # fig.update_layout(
    #     margin=dict(l=20, r=20, t=20, b=20),
    #     paper_bgcolor="LightSteelBlue"
    #     )

    fig2.update_geos(fitbounds='locations', visible=False)

    return fig, fig2



if __name__ == '__main__':
    app.run_server(debug=True)


