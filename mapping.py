'''
A file to create our website in plotly
'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# https://plotly.com/python/choropleth-maps/
# https://www.youtube.com/watch?v=hSPmj7mK6ng&list=TLPQMDIwMzIwMjK-RX-K6Ja5bw&index=5

app = dash.Dash(__name__)

# -----------------------------------------------------------
# Import and clean data
import scraping.get_census_data as cen_scrape

# TBD if we want to just have demos in a ready made csv to avoid scarping; I think so ###############################################
census_data = cen_scrape.go(True)
census_data["cca"] = census_data["cca"].astype(str)
geojson = pd.read_json("data/community_areas.geojson")

# -----------------------------------------------------------
# App layout

app.layout = html.Div([
    html.H1("How demographics impact 311 data", style={'text-align': 'center'}),

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
                 style = {'width': '40%'}
                 ),
    html.Br(),

    dcc.Graph(id='demo_map', figure={})
])

# -----------------------------------------------------------
# Connect the Plotly graphs with Dash Componenets
@app.callback(
    Output(component_id = 'demo_map', component_property='figure'),
    [Input(component_id = 'select_race', component_property='value')])

def update_graph(race):
    '''
    Updates graph based on race selected
    '''
    fig = px.choropleth(
        data_frame=census_data,
        geojson=geojson,
        color=race,
        locations="cca",
        featureidkey="properties.area_numbe",
        projection="mercator", 
        range_color=[0,1]
        )

    fig.update_geos(fitbounds='locations', visible=False)       

    return fig


# data_json = data['features']
# data.features[0]["properties"]["area_numbe"]
# data2 = pd.read_csv('data/CommAreas.csv')

if __name__ == '__main__':
    app.run_server(debug=True)


