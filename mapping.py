'''
A file to create our website in plotly
'''
# LIST OF THINGS LATER?
# do color scheme 0 to max(percent of category) instead of 0-100 (change per income vs. race vs. unemployment)
# add filter for other categories (subfilters)
# connect 311 data to 2nd graph
# fix hover labels (show percentages instead of ratio)
# replicate with scatterplot and bar plot (on the bottom)

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
import numpy as np

# https://plotly.com/python/choropleth-maps/
# https://www.youtube.com/watch?v=hSPmj7mK6ng&list=TLPQMDIwMzIwMjK-RX-K6Ja5bw&index=5

app = dash.Dash(__name__)

# -----------------------------------------------------------
# Import and clean data
census_data = pd.read_csv("data/census_demos.csv")
census_data["cca_num"] = census_data["cca_num"].astype(str)
geojson = gpd.read_file("data/community_areas.geojson")

# Create dictionary needed for multi-layer drop level
all_options = {
    'Race': {"White": "White",
             "Black": "Black_or_African_American",
             "Native American": "American_Indian_or_Alaska_Native",
             "Asian": "Asian",
             "Native Hawaiian or Other Pacific Islander": "Native_Hawaiian_or_Other_Pacific_Islander",
             "Other single race": "some_other_race_alone",
             "2+ races": "two_or_more_races"},
    'Min annual income': {"$0": "LTM_income_sub_10k",
                         "$10k": "LTM_income_10-15k",
                         "$15k": "LTM_income_15_20k",
                         "$20k": "LTM_income_20_25k",
                         "$25k": "LTM_income_25_30k",
                         "$30k": "LTM_income_30_35k",
                         "$35k": "LTM_income_35_40k",
                         "$40k": "LTM_income_40_45k",
                         "$45k": "LTM_income_45_50k",
                         "$50k": "LTM_income_50_60k",
                         "$60k": "LTM_income_60_75k",
                         "$75k": "LTM_income_75_100k",
                         "$100k": "LTM_income_100_125k",
                         "$125k": "LTM_income_125_150k",
                         "$150k": "LTM_income_150_200k",
                         "$200k": "LTM_income_200k+"},
    #'Income': 
    # 
             #{'Min': [("$0", "LTM_income_sub_10k"),
    #                    ("$10k", "LTM_income_10-15k"),
    #                    ("$15k", "LTM_income_15_20k"),
    #                    ("$20k", "LTM_income_20_25k"),
    #                    ("$25k", "LTM_income_25_30k"),
    #                    ("$30k", "LTM_income_30_35k"),
    #                    ("$35k", "LTM_income_35_40k"),
    #                    ("$40k", "LTM_income_40_45k"),
    #                    ("$45k", "LTM_income_45_50k"),
    #                    ("$50k", "LTM_income_50_60k"),
    #                    ("$60k", "LTM_income_60_75k"),
    #                    ("$75k", "LTM_income_75_100k"),
    #                    ("$100k", "LTM_income_100_125k"),
    #                    ("$125k", "LTM_income_125_150k"),
    #                    ("$150k", "LTM_income_150_200k"),
    #                    ("$200k", "LTM_income_200k+")],
    #            'Max': [("$10k", "LTM_income_sub_10k"),
    #                   ("$15k", "LTM_income_10-15k"),
    #                   ("$20k", "LTM_income_15_20k"),
    #                   ("$25k", "LTM_income_20_25k"),
    #                   ("$30k", "LTM_income_25_30k"),
    #                   ("$35k", "LTM_income_30_35k"),
    #                   ("$40k", "LTM_income_35_40k"),
    #                   ("$45k", "LTM_income_40_45k"),
    #                   ("$50k", "LTM_income_45_50k"),
    #                   ("$60k", "LTM_income_50_60k"),
    #                   ("$75k", "LTM_income_60_75k"),
    #                   ("$100k", "LTM_income_75_100k"),
    #                   ("$125k", "LTM_income_100_125k"),
    #                   ("$150k", "LTM_income_125_150k"),
    #                   ("$200k", "LTM_income_150_200k"),
    #                   ("No max", "LTM_income_200k+")]},
    'Unemployment': {"Percent unemployed": "percent_unemployed"}
    }
maximum_income_d = {"$10k": "LTM_income_sub_10k",
                    "$15k": "LTM_income_10-15k",
                    "$20k": "LTM_income_15_20k",
                    "$25k": "LTM_income_20_25k",
                    "$30k": "LTM_income_25_30k",
                    "$35k": "LTM_income_30_35k",
                    "$40k": "LTM_income_35_40k",
                    "$45k": "LTM_income_40_45k",
                    "$50k": "LTM_income_45_50k",
                    "$60k": "LTM_income_50_60k",
                    "$75k": "LTM_income_60_75k",
                    "$100k": "LTM_income_75_100k",
                    "$125k": "LTM_income_100_125k",
                    "$150k": "LTM_income_125_150k",
                    "$200k": "LTM_income_150_200k",
                    "No max": "LTM_income_200k+"}

# -----------------------------------------------------------
# App layout

app.layout = dbc.Container([
    dbc.Row(dbc.Col(
        html.H1("How Neighborhood Demographics Impact 311 Responsiveness", style={'text-align': 'center', 'font-family': 'Helvetica'}))#,
    ),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="select_first_filter",
                        options =[
                            {"label": "Race", "value": "Race"},
                            {"label": "Minimum annual income", "value": "Min annual income"},
                            {"label": "Unemployment", "value": "Unemployment"}],
                        multi = False,
                        value = "Race",
                        style = {'width': '40%', 'display': 'inline-block', 'text-align': 'center', 'font-family': 'Helvetica'}
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
                        style = {'width': '40%', 'display': 'inline-block', 'text-align': 'center', 'font-family': 'Helvetica'}
                        ),
            # Graph 1 second-level dropdown
            dcc.Dropdown(id="secondary_filter",
                         style = {'width': '40%', 'display': 'inline-block', 'text-align': 'center'}
                         ),

            ])

        ]),

    dbc.Row([
        dbc.Col([

            dcc.Graph(id='demo_map', figure={}, style = {'display': 'inline-block', 'width': '80vh', 'height': '90vh'}),
            dcc.Graph(id='demo_map2', figure={}, style = {'display': 'inline-block', 'width': '80vh', 'height': '90vh'})
            
            ])

        ])

    ], fluid=True)

# -----------------------------------------------------------
# Connect the Plotly graphs with Dash Componenets
@app.callback(
    dash.dependencies.Output('secondary_filter', 'options'),
    [dash.dependencies.Input('select_first_filter', 'value')]
    )

# def get_data(option):
#     '''
#     Updates data frame for filtering values
#     '''
#     if option == 'Race' or option == 'Unemployment':
#         output = census_data[['cca_name', 'cca_']

def set_second_options(option):
    '''
    Updates secondary filter options
    '''
    return [{'label': k, 'value': v} for k,v in all_options[option].items()]

@app.callback(
    dash.dependencies.Output('secondary_filter', 'value'),
    [dash.dependencies.Input('secondary_filter', 'options')]
    )

def set_second_value(options):
    '''
    Updates secondary default value
    '''
    return options[0]['value']

@app.callback(
    [Output(component_id = 'demo_map', component_property='figure'),
    Output(component_id = 'demo_map2', component_property='figure')],

    [Input(component_id = 'secondary_filter', component_property='value'),
    Input(component_id = 'select_race2', component_property='value')]
    )

def update_graph(race, race2):
    '''
    Updates graph based on race selected
    '''

    # Set zoom bounds

    fig = px.choropleth_mapbox(
        data_frame=census_data,
        geojson=geojson,
        color=race,
        color_continuous_scale='blues',
        locations="cca_num",
        zoom=9, 
        center = {"lat": 41.8, "lon": -87.75},
        opacity=0.8,
        featureidkey="properties.area_numbe",
        mapbox_style="open-street-map",
        # projection="mercator",
        hover_name="cca_name",
        hover_data=[race],
        range_color=[0,100],
        title=f"% {race} by Chicago Neighobrhood (ACS 2019)"
        # width=400,
        # height=800
        )

    fig2 = px.choropleth_mapbox(
        data_frame=census_data,
        geojson=geojson,
        color=race2,
        color_continuous_scale='blues',
        locations="cca_num",
        zoom=9, 
        center = {"lat": 41.8, "lon": -87.75},
        opacity=0.8,
        featureidkey="properties.area_numbe",
        mapbox_style="open-street-map",
        # projection="mercator", 
        range_color=[0,100],
        hover_name="cca_name",
        hover_data=[race2],
        title=f"% {race2} by Chicago Neighborhood (Chicago 311 Requests)"
        # width=400,
        # height=800
        )
    
    fig.update_geos(fitbounds='locations', visible=False#,
    #   center=dict(lon=41.8, lat=-87.75)
      )
    # fig.update_traces(hoverinfo='location+cca_name')
    
    # fig.update_layout(
    #     margin=dict(l=40, r=40, t=40, b=40)#,
    #     # paper_bgcolor="LightSteelBlue"
    #     )

    fig2.update_geos(fitbounds='locations', visible=False)

    return fig, fig2



if __name__ == '__main__':
    app.run_server(debug=True)


