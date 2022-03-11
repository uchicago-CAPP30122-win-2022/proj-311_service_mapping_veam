'''
A file to create our website in plotly
'''
# LIST OF THINGS LATER?
# connect 311 data to 2nd graph
# replicate with scatterplot and bar plot (on the bottom)
# Get clone venv stuff check Lamont later this week
# Import smaller modules to get component (Dash documentation models)
# First map tooltip: remove cca_num and one of the %'s
# Dynamic range for y-axes first map - just for income

# ---- TO DO: BAR GRAPH 2
# need to fix # requests per 1k -- currently is not per 1k
# convert into days
# hover labels/tips
# height of both bar graphs
# resize graphs (primary should be bigger)
# second bar graph title cuts off if too long
# Need overall chicago stats

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
from scraping.create_cca_tract_dict import create_dictionaries

# https://plotly.com/python/choropleth-maps/
# https://www.youtube.com/watch?v=hSPmj7mK6ng&list=TLPQMDIwMzIwMjK-RX-K6Ja5bw&index=5

app = dash.Dash("Final project", external_stylesheets=[dbc.themes.SUPERHERO])

# -----------------------------------------------------------
# Import and clean data
census_data = pd.read_csv("data/census_demos.csv")
census_data["cca_num"] = census_data["cca_num"].astype(str)
geojson = gpd.read_file("data/community_areas.geojson")
service_311_bar = pd.read_csv("data/311_census_bar.csv")

# -----------------------------------------------------------
# Set up dictionaries for filtering data
_, comm_area_dict = create_dictionaries()

neighborhoods = []
for neighbordhood in comm_area_dict.values():
    neighborhoods.append(neighbordhood)

neighbordhoods = sorted(neighborhoods)

neighborhood_to_cca_num = {v: k for k,v in comm_area_dict.items()}

# Set up dictionaries for filtering data
race_cols = ["White", "Black_or_African_American",
             "American_Indian_or_Alaska_Native", "Asian",
             "Native_Hawaiian_or_Other_Pacific_Islander",
             "some_other_race_alone", "two_or_more_races"]
unemployment_cols = ['percent_unemployed']
income_cols = ["LTM_income_sub_10k", "LTM_income_10-15k", "LTM_income_15_20k",
                "LTM_income_20_25k", "LTM_income_25_30k", "LTM_income_30_35k",
                "LTM_income_35_40k", "LTM_income_40_45k", "LTM_income_45_50k",
                "LTM_income_50_60k", "LTM_income_60_75k", "LTM_income_75_100k",
                "LTM_income_100_125k", "LTM_income_125_150k",
                "LTM_income_150_200k", "LTM_income_200k+"]
max_income_tuples = [("$10k", "LTM_income_sub_10k"),
                     ("$15k", "LTM_income_10-15k"),
                     ("$20k", "LTM_income_15_20k"),
                     ("$25k", "LTM_income_20_25k"),
                     ("$30k", "LTM_income_25_30k"),
                     ("$35k", "LTM_income_30_35k"),
                     ("$40k", "LTM_income_35_40k"),
                     ("$45k", "LTM_income_40_45k"),
                     ("$50k", "LTM_income_45_50k"),
                     ("$60k", "LTM_income_50_60k"),
                     ("$75k", "LTM_income_60_75k"),
                     ("$100k", "LTM_income_75_100k"),
                     ("$125k", "LTM_income_100_125k"),
                     ("$150k", "LTM_income_125_150k"),
                     ("$200k", "LTM_income_150_200k"),
                     ("No max", "LTM_income_200k+")]

# Create dictionaries needed for multi-layer drop level and outputting them
race_label_to_value = {"White": "White",
                       "Black": "Black_or_African_American",
                       "Native American": "American_Indian_or_Alaska_Native",
                       "Asian": "Asian",
                       "Native Hawaiian / Pacific Islander": "Native_Hawaiian_or_Other_Pacific_Islander",
                       "Other single race": "some_other_race_alone",
                       "2+ races": "two_or_more_races"}
race_value_to_label = {v: k for k,v in race_label_to_value.items()}

min_income_label_to_value = {"$0": "LTM_income_sub_10k",
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
                             "$200k": "LTM_income_200k+"}
min_income_value_to_label = {v: k for k,v in min_income_label_to_value.items()}
max_income_value_to_label = {value: label for label, value in max_income_tuples}

unemployment_label_to_value = {"Unemployed": "percent_unemployed"}
unemployment_value_to_label = {v: k for k,v in unemployment_label_to_value.items()}

second_filter = {
    'Race': race_label_to_value,
    'Range of annual incomes': min_income_label_to_value,
    'Unemployment': unemployment_label_to_value
    }
third_filter = {'Race': {"--": "--"},
    # Not in use 'Range of annual incomes': 
                            #    {"$10k": "LTM_income_sub_10k",
                            #     "$15k": "LTM_income_10-15k",
                            #     "$20k": "LTM_income_15_20k",
                            #     "$25k": "LTM_income_20_25k",
                            #     "$30k": "LTM_income_25_30k",
                            #     "$35k": "LTM_income_30_35k",
                            #     "$40k": "LTM_income_35_40k",
                            #     "$45k": "LTM_income_40_45k",
                            #     "$50k": "LTM_income_45_50k",
                            #     "$60k": "LTM_income_50_60k",
                            #     "$75k": "LTM_income_60_75k",
                            #     "$100k": "LTM_income_75_100k",
                            #     "$125k": "LTM_income_100_125k",
                            #     "$150k": "LTM_income_125_150k",
                            #     "$200k": "LTM_income_150_200k",
                            #     "No max": "LTM_income_200k+"},
    'Unemployment': {"--": "--"}
    } 

dict_responsetime = {
    "perc_resol_less_than_1": "% Resolved in < 1 min",
    "perc_resol_1_min_1_hr": "% Resolved in 1 min - < 1 hr",
    "perc_resol_1_hr_12_hr": "% Resolved in 1 hr - < 12 hr",
    "perc_resol_12_24_hr": "% Resolved in 12 hr - < 24 hr",
    "perc_resol_1_3_day": "% Resolved in 1 - <3 days",
    "perc_resol_3_7_day": "% Resolved in 3 - <7 days",
    "perc_resol_7_14_day": "% Resolved in 7 - <14 days",
    "perc_resol_14_30_day": "% Resolved in 14 - <30 days",
    "perc_resol_1_3_month": "% Resolved in 1 - <3 months",
    "perc_resol_3_12_month": "% Resolved in 3 - <12 months",
    "perc_resol_1_year_plus": "% Resolved in 1+ years",
    "perc_resol_unresolved": "% Left Unresolved"
    }

dict_311_stat = {
    "total_reqs": "Number of Requests (per 1000 people)",
    "avg_resol_time": "Avg. Resolution Time (days)",
    "median_resol_time": "Median Resolution Time (days)"
    }

dropdown_style_d = {'display': 'inline-block',
                    'text-align': 'center',
                    'font-family': 'Helvetica',
                    'color': '#4c9be8',
                    'width': '60%'}

# -----------------------------------------------------------
# App layout

demo_map = [
    # Demo map
        html.Br(),
        dbc.Row(html.H3("Filter: Census Demographics"),style={'text-align': 'center'},justify='center'),
        html.Br(),
        dbc.Row(
            dcc.Dropdown(id="primary_filter",
                         options =[
                            {"label": "Race", "value": "Race"},
                            {"label": "Range of annual incomes", "value": "Range of annual incomes"},
                            {"label": "Percent unemployed", "value": "Unemployment"}],
                         multi = False,
                         value = "Race",
                         style = dropdown_style_d,
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Dropdown(id="secondary_filter",
                         style = dropdown_style_d
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Dropdown(id="tertiary_filter",
                         style = dropdown_style_d,
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Graph(id='demo_map', figure={'layout': {'paper_bgcolor': "#0f2537",
                                                        'plot_bgcolor': "#0f2537"}}, 
                      style = {'display': 'inline-block', 'width': '80vh',
                               'height': '90vh'},
                      ),
            justify='center'
            )
    ]
resolution_times_graph = [
    # 311 data map
        html.Br(),
        dbc.Row(html.H3("Filter: 311 Service Request Types"),style={'text-align': 'center'},justify='center'),
        html.Br(),
        dbc.Row(
            dcc.Dropdown(id="select_race2",
                        options =[ {'label': k, 'value': v} for k, v in race_label_to_value.items()],
                        multi = False,
                        value = "White",
                        style = dropdown_style_d
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Dropdown(id="secondary_filter2",
                         style = dropdown_style_d,
                         multi = False,
                         options = {"--": "--"},
                         value = "--",
                         disabled=True
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Dropdown(id="tertiary_filter2",
                         style = dropdown_style_d,
                         multi = False,
                         options = {"--": "--"},
                         value = "--",
                         disabled=True
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Graph(id='demo_map2', figure={'layout': {'paper_bgcolor': "#0f2537",
                                                        'plot_bgcolor': "#0f2537"}}, 
                       style = {'display': 'inline-block', 'width': '80vh', 'height': '90vh'}),
            justify='center'
        )
    ]

middle_row_content = [
    # For bar graph
    html.Br(),
    dbc.Row(html.H3("Filter: Neighborhood for Resolution Times of 311 Requests"),style={'text-align': 'center'},justify='center'),
    html.Br(),
    dbc.Row(
            dcc.Dropdown(id="bar_cca",
                        options =[ {'label': hood, 'value': neighborhood_to_cca_num[hood]} for hood in neighbordhoods],
                        multi = False,
                        value = 41,
                        style = dropdown_style_d
                        ),
                        justify='center'
            ),
    dbc.Row(html.Br()),

    dbc.Col([
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(
                dcc.Graph(id='bar_graph', figure={}, style = {'display': 'inline-block', 'width': '80vh', 'height': '90vh'}),
                justify='center'
                )
        ]),

    # Neighborhood bar graph
    dbc.Col([
        dbc.Row(
            dcc.Dropdown(id="bar2_311",
                        options =[{'label': v, 'value':k} for k, v in dict_311_stat.items()],
                        multi = False,
                        value = 'avg_resol_time',
                        style = dropdown_style_d
                        ),
                        justify='center'
            ),
        dbc.Row(
            dcc.Graph(id='bar2_graph', figure={'layout': {'paper_bgcolor': "#0f2537",
                                                        'plot_bgcolor': "#0f2537"}}, 
                       style = {'display': 'inline-block', 'width': '80vh', 'height': '90vh'}),
            justify='center'
            )
        ])

    ]

app.layout = dbc.Container([
    html.Br(),
    dbc.Row(
        html.H1("How Neighborhood Demographics Impact 311 Responsiveness",
                style={'text-align': 'center',
                       'font-family': 'Helvetica',
                       'font-size': '2.5rem',
                       'font-color': '#fff'})
        ),

    dbc.Row([dbc.Col(demo_map), dbc.Col(resolution_times_graph)]),
    dbc.Row(html.Br()),
    dbc.Row(middle_row_content),
    dbc.Row("Sources: Chicago 311 Service Request Data (Chicago Data Portal) & American Community Survey (2019)"),
    dbc.Row(html.Br())
    ]
    ,fluid=True, style={'backgroundColor':'#0f2537'}
    )

# -----------------------------------------------------------
# Connect the Plotly graphs with Dash Componenets
# Census demo map: First and second filter
@app.callback(
    dash.dependencies.Output('secondary_filter', 'options'),
    dash.dependencies.Output('secondary_filter', 'value'),
    dash.dependencies.Output('secondary_filter', 'disabled'),
    [dash.dependencies.Input('primary_filter', 'value')]
    )

def set_second_options_and_value(option):
    '''
    Updates secondary filter options
    '''
    options = [{'label': k, 'value': v} for k,v in second_filter[option].items()]
    disabled = False
    if option == 'Unemployment':
        disabled = True
    return options, options[0]['value'], disabled

# Census demo map: Third filter
@app.callback(
    dash.dependencies.Output('tertiary_filter', 'options'),
    dash.dependencies.Output('tertiary_filter', 'value'),
    dash.dependencies.Output('tertiary_filter', 'disabled'),
    [dash.dependencies.Input('secondary_filter', 'value'),
     dash.dependencies.Input('primary_filter', 'value')]
    )

def set_third_options(option, first_filter):
    '''
    Updates third filter options
    '''
    if first_filter != 'Range of annual incomes':
        options =  [{'label': k, 'value': v} for k,v in third_filter[first_filter].items()]
        disabled = True
    else:
        idx = income_cols.index(option)
        options =  [{'label': l, 'value': v} for l,v in max_income_tuples[idx:]]
        disabled = False
    return options, options[0]['value'], disabled
    

# Make census demo map
@app.callback(
    Output(component_id = 'demo_map', component_property='figure'),
    [Input(component_id = 'primary_filter', component_property='value'),
    Input(component_id = 'secondary_filter', component_property='value'),
    Input(component_id = 'tertiary_filter', component_property='value')]
    )

def update_census_map(overall_filter, demo, secondary_demo):
    '''
    Updates census graph based on demo selected
    '''
    if overall_filter == 'Race':
        output_col = census_data[demo].copy()
    elif overall_filter == 'Unemployment':
        output_col = census_data[demo].copy()
    else:
        potential_incomes = census_data[income_cols].copy()
        cols = potential_incomes.columns
        min_idx = cols.get_loc(demo)
        max_idx = cols.get_loc(secondary_demo)
        to_sum = potential_incomes.iloc[:, min_idx: max_idx + 1]
        output_col = to_sum.sum(axis=1)

    # Set up data to output
    demo_output = census_data[['cca_num', 'cca_name']].copy()
    demo_output.loc[:, 'output_col'] = output_col
    
    # Set up title info and output_col_title
    if overall_filter == 'Race':
        title_label = race_value_to_label[demo]
        output_hover_data = "%" + title_label # Create column name for hover_data
        demo_output[output_hover_data] = demo_output['output_col']
    elif overall_filter == 'Unemployment':
        title_label = unemployment_value_to_label[demo]
        output_hover_data = '% Unemp.' # Create column name for hover_data
        demo_output[output_hover_data] = demo_output['output_col']
    else:
        min_label = min_income_value_to_label[demo]
        max_label = max_income_value_to_label[secondary_demo]
        if max_label == "No max":
            title_label = "making over " + min_label + " per year"
            output_hover_data = '% >' + min_label # Create column name for hover_data
            demo_output[output_hover_data] = demo_output['output_col']
        else:
            title_label = "making between " + min_label + " - " + max_label + " per year"
            output_hover_data = "% b/t " + min_label + " - " + max_label # Create column name for hover_data
            demo_output[output_hover_data] = demo_output['output_col']
    # Set the actual reference column
    demo_output['%'] = demo_output[output_hover_data]
    
    # Set zoom bounds
    if overall_filter == 'Unemployment':
        range_lst = [0,50]
    else:
        range_lst = [0,100]

    fig = px.choropleth_mapbox(
        data_frame=demo_output,
        geojson=geojson,
        color='%',
        color_continuous_scale='blues',
        locations="cca_num",
        zoom=9, 
        center = {"lat": 41.8, "lon": -87.75},
        opacity=0.8,
        featureidkey="properties.area_numbe",
        mapbox_style="open-street-map",
        hover_name="cca_name",
        hover_data={output_hover_data: ':.2f'},
        range_color=range_lst,
        title=f"% {title_label} by Chicago Neighobrhood"
        )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(paper_bgcolor="#0f2537", font_color = '#fff')

    return fig

# Update 311 map
@app.callback(
    Output(component_id = 'demo_map2', component_property='figure'),
    [Input(component_id = 'select_race2', component_property='value')]
    )

def update_census_map(race2):
    '''
    Updates 311 graph based on demo selected
    '''
    fig = px.choropleth_mapbox(
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
        range_color=[0,100],
        hover_name="cca_name",
        hover_data=[race2],
        title=f"% {race2} by Chicago Neighborhood (Chicago 311 Requests)"
        )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(paper_bgcolor="#0f2537", font_color = '#fff')  

    return fig


# Make bar graph
@app.callback(
    [Output(component_id = 'bar_graph', component_property='figure'),
    Output(component_id = 'bar2_graph', component_property='figure')],
    [Input(component_id = 'bar_cca', component_property='value'),
    Input(component_id = 'bar2_311', component_property='value')]
    )

def update_bar(neighborhood, statistic_311):
    '''
    '''

    #Find overall Chicago 311 statistics
    # fill this in here

    bar_data_filter = service_311_bar[(service_311_bar['community_area'] == neighborhood)]
    bar_data_filter = bar_data_filter.set_index('year').T.rename_axis('Variable').reset_index()

    # Filter data for main bar graph
    drop1 = ['community_area', 'total_reqs', 'avg_resol_time', 'median_resol_time']
    data_melt = bar_data_filter[~bar_data_filter['Variable'].isin(drop1)]
    data_melt = pd.melt(data_melt, id_vars=['Variable'], var_name='year', value_name='value')
    data_melt['value'] = round(data_melt['value'] * 100, 2)

    # Filter data for secondary bar graph
    drop2 = [key for key in dict_responsetime.keys()]
    drop2.extend([d for d in drop1 if d != statistic_311])
    data2_melt = bar_data_filter[~bar_data_filter['Variable'].isin(drop2)]
    data2_melt = pd.melt(data2_melt, id_vars=['Variable'], var_name='year', value_name='value')

    title1_label = comm_area_dict[neighborhood]
    title2_label = dict_311_stat[statistic_311]


    # Bar Graph 1: Primary
    bar = px.bar(
        data_frame=data_melt,
        x = 'Variable',
        y = 'value', 
        barmode='group',
        color='year',
        color_discrete_sequence=[px.colors.qualitative.Safe[0], px.colors.qualitative.Vivid[7], "#00558c"],
        title=f"311 Request Response Time in {title1_label}",
        labels={    "Variable": "Responsiveness Time",
                    "value": "% Requests Completed",
                    "year": "Year"},
        
        width=800,
        height=600
        )
    bar.update_xaxes(
        type='category',
        ticktext = [v for _, v in dict_responsetime.items()],
        tickvals = [k for k, _ in dict_responsetime.items()]
        )
    bar.update_yaxes(
        ticksuffix = "%"
        )
    bar.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537", font_color = '#fff')

    # Bar Graph 2: Secondary (Neighborhood Specific)
    bar2 = px.bar(
        data_frame=data2_melt,
        x = 'Variable',
        y = 'value', 
        barmode='group',
        color='year',
        color_discrete_sequence=[px.colors.qualitative.Safe[0], px.colors.qualitative.Vivid[7], "#00558c"],
        title=f"311 Request Statistics: {title2_label} for {title1_label}",
        labels={    "Variable": f"{title1_label}",
                    "value": title2_label,
                    "year": "Year"},
        width=800,
        height=600
        )
    bar2.update_xaxes(
        showticklabels=False
        )
    bar2.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537", font_color = '#fff')

    return bar, bar2


if __name__ == '__main__':
    app.run_server(debug=True)


