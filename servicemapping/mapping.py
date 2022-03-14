'''
A file to create our website in plotly
'''
# TBUs
# Get clone venv stuff check Lamont later this week: MAC USERS
# Import smaller modules to get component (Dash documentation models)
# Doc strings
# make writeup

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np
from data_pull.census.create_cca_tract_dict import create_dictionaries
import statsmodels

app = dash.Dash("Final project", external_stylesheets=[dbc.themes.SUPERHERO])

# -----------------------------------------------------------
# Import and clean data
census_data = pd.read_csv("data/census_demos.csv")
census_data["cca_num"] = census_data["cca_num"].astype(str)
geojson = gpd.read_file("data/community_areas.geojson")

service_311_bar = pd.read_csv("data/311_census_bar.csv")
df_311_census = pd.read_csv("data/sr_census_df.csv")
chicago_311_avg = pd.read_csv("data/chicago_df.csv")

to_use_to_make_per_1k = df_311_census[['cca_num_x', 'total_num_race_estimates']]
service_311_bar = service_311_bar.merge(to_use_to_make_per_1k,
                                        left_on="community_area",
                                        right_on="cca_num_x")
del service_311_bar["cca_num_x"]
service_311_bar['sr_per_1000'] = 1000 * (service_311_bar['total_reqs'] /
                                 service_311_bar['total_num_race_estimates'])

# Round data off
for df in [service_311_bar, df_311_census]:
    df['avg_resol_time'] = df['avg_resol_time']/(24*60)
    df['avg_resol_time'] = df['avg_resol_time'].round(2)
    df['median_resol_time'] = df['median_resol_time']/(24*60)
    df['median_resol_time'] = df['median_resol_time'].round(2)
    df['sr_per_1000'] = df['sr_per_1000'].round(0)

df_311_census['Top 311 issue'] = df_311_census['top_1']
df_311_census['2nd issue'] = df_311_census['top_2']
df_311_census['3rd issue'] = df_311_census['top_3']
df_311_census['sr_per_1000'] = df_311_census['sr_per_1000'] // 3

df_311_census['perc_resol_unresolved'] = df_311_census['perc_resol_unresolved'] * 100
df_311_census['perc_resol_unresolved'] = df_311_census['perc_resol_unresolved'].round(2)



# -----------------------------------------------------------
# Set up dictionaries for filtering data
_, comm_area_dict = create_dictionaries()

neighborhoods = []
for neighbordhood in comm_area_dict.values():
    neighborhoods.append(neighbordhood)

neighborhoods = sorted(neighborhoods)

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
third_filter = {'Race': {"--": "--"}, 'Unemployment': {"--": "--"}} 

# Second map filter
map_311_filter = {
    "sr_per_1000": "Avg. Annual Num. Service Requests (per 1000 people)",
    "avg_resol_time": "Avg. Resolution Time (days)",
    "median_resol_time": "Median Resolution Time (days)"}

# For bar plots
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
    "sr_per_1000": "Annual Number of 311 Requests (per 1000 people)",
    "avg_resol_time": "Avg. 311 Request Resolution Time (days)",
    "median_resol_time": "Median 311 Request Resolution Time (days)"
    }

# For scatter plot
dict_scatter_y = {
    "sr_per_1000": "Avg. Annual Num. Service Requests per 1000 people",
    "avg_resol_time": "Avg. Resolution Time (days)",
    "median_resol_time": "Median Resolution Time (days)",
    "perc_resol_unresolved": "Percent Left Unresolved",
    'Abandoned Vehicle Complaint': 'Abandoned Vehicle Complaint',
    'Garbage Cart Maintenance': 'Garbage Cart Maintenance', 
    'Graffiti Removal Request': 'Graffiti Removal Request',
    'Pothole in Street Complaint': 'Pothole in Street Complaint',
    'Rodent Baiting/Rat Complaint': 'Rodent Baiting/Rat Complaint',
    'Street Light Out Complaint': 'Street Light Out Complaint',
    'Tree Trim Request': 'Tree Trim Request',
    'Weed Removal Request': 'Weed Removal Request'
    }

dict_scatter_x = race_value_to_label
dict_scatter_x["percent_unemployed"] = "Unemployed"


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
                               'height': '50vh'},
                      ),
            justify='center'
            )
    ]
resolution_times_graph = [
    # 311 data map
        html.Br(),
        dbc.Row(html.H3("Filter: 311 Service Request Summary Stats"),style={'text-align': 'center'},justify='center'),
        html.Br(),
        html.Br(),
        dbc.Row(
            dcc.Dropdown(id="311_map_filter",
                        options = [{'label': v, 'value':k} for k, v in map_311_filter.items()],
                        multi = False,
                        value = "sr_per_1000",
                        style = dropdown_style_d
                        ),
                justify='center'
                ),
        dbc.Row(html.Br()),
        dbc.Row(html.Br()),
        dbc.Row(
            dcc.Graph(id='311_map', figure={'layout': {'paper_bgcolor': "#0f2537",
                                                        'plot_bgcolor': "#0f2537"}}, 
                       style = {'display': 'inline-block', 'width': '80vh', 'height': '50vh'}),
            justify='center'
        )
    ]

# Middle row - bar graphs
middle_row_content = [
    # For bar graph
    dbc.Row(html.Br()),
    dbc.Row(html.H3("Filter: Neighborhood for Resolution Times of 311 Requests"),style={'text-align': 'center'},justify='center'),
    dbc.Row(html.Br()),
    dbc.Row(
            dcc.Dropdown(id="bar_cca",
                        options =[ {'label': hood, 'value': neighborhood_to_cca_num[hood]} for hood in neighborhoods],
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
        dbc.Row(html.Br()),
        dbc.Row(
                dcc.Graph(id='bar_graph', figure={}, style = {'display': 'inline-block', 'width': '80vh', 'height': '50vh'}),
                justify='center'
                )
        ]),

    # Neighborhood bar graph
    dbc.Col([
        dbc.Row(html.H5("Filter: 311 Requests Summary Stats"),style={'text-align': 'center'},justify='center'),
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
                       style = {'display': 'inline-block', 'width': '80vh', 'height': '50vh'}),
            justify='center'
            )
        ])

    ]


dropdown_style_s = dropdown_style_d.copy()
dropdown_style_s['width'] = '50%'

# Bottom row - scatterplot
bottom_row_content = [
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    dbc.Row(html.H3("Filter: Plotting Census Demographics on 311 Service Request Data"),style={'text-align': 'center'},justify='center'),
    dbc.Row(html.Br()),

    dbc.Row([
        dbc.Col([
            dbc.Row(html.H5("Select a Census Demo"),style={'text-align': 'center'},justify='center'),
            dbc.Row(
            dcc.Dropdown(id="primary_scatter",
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
            dcc.Dropdown(id="secondary_scatter",
                         style = dropdown_style_d
                        ),
                justify='center'
                ),
        dbc.Row(
            dcc.Dropdown(id="tertiary_scatter",
                         style = dropdown_style_d,
                        ),
                justify='center'
                )
        ]),
        dbc.Col([
            dbc.Row(html.H5("Select 311 info"),style={'text-align': 'center'},justify='center'),
            dbc.Row(
                # Col: Insert Dropdown 1
                dcc.Dropdown(id="scatter_y",
                    options =[ {'label': v, 'value': k} for k, v in dict_scatter_y.items()],
                    multi = False,
                    value = "sr_per_1000",
                    style = dropdown_style_d
                    ),
                justify='center')
            ]),
    ]),
    dbc.Row(
        # Insert scatterplot map
        dcc.Graph(id='scatter', figure={'layout': {'paper_bgcolor': "#0f2537",
                                            'plot_bgcolor': "#0f2537"}}, 
            style = {'display': 'inline-block', 'width': '80vh', 'height': '50vh'}),
            justify='center'
        ),
    dbc.Row(html.Br())
    ]

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
        output_hover_data = "% " + title_label # Create column name for hover_data
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
    
    # Set color bounds
    max_val = demo_output['%'].max()
    if max_val < 1:
        max_val_denom = .1
        max_val = max_val_denom * -(-max_val//max_val_denom)
    else:
        max_val_str = str(min(99, int(max_val))) # In case we have a 100% cca
        first_digit = str(int(max_val_str[0]) + 1)
        num_zero = len(max_val_str) - 1
        max_val = int(first_digit + num_zero * "0")

    if overall_filter == 'Unemployment':
        ranges = [0,40]
    else:
        ranges = [0,max_val]
        
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
        hover_data={output_hover_data: ':.2f',
                    'cca_num': False,
                    '%': False},
        range_color=ranges,
        title=f"% {title_label} by Chicago Neighborhood"
        )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(paper_bgcolor="#0f2537", font_color = '#fff')

    return fig


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
        title=f"{map_311_filter[filter_for_311]} by Chicago Neighborhood"
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

    bar_data_filter = service_311_bar[(service_311_bar['community_area'] == neighborhood)]
    bar_data_filter = bar_data_filter.set_index('year').T.rename_axis('Variable').reset_index()

    # Filter data for main bar graph
    drop1 = ['community_area', 'total_reqs', 'avg_resol_time', 'median_resol_time', 'sr_per_1000', 'total_num_race_estimates']
    pre_melt = bar_data_filter[~bar_data_filter['Variable'].isin(drop1)]
    data_melt = pd.melt(pre_melt, id_vars=['Variable'], var_name='year', value_name='value')
    data_melt['value'] = round(data_melt['value'] * 100, 2)

    # Filter data for secondary bar graph
    drop2 = [key for key in dict_responsetime.keys()]
    drop2.extend([d for d in drop1 if d != statistic_311])
    data2_melt = bar_data_filter[~bar_data_filter['Variable'].isin(drop2)]
    data2_melt = pd.melt(data2_melt, id_vars=['Variable'], var_name='year', value_name='value')

    # Title labels
    title1_label = comm_area_dict[neighborhood]
    title2_label = dict_311_stat[statistic_311]

    # Bring in Chicago info
    chicago_avgs = chicago_311_avg[['year', statistic_311]].copy()
    chicago_avgs.columns = ['year', 'value']
    chicago_avgs['Variable'] = 'Chicago Avg.'

    data2_melt['Variable'] = title1_label
    data2_melt = pd.concat([data2_melt, chicago_avgs])

    # Set y axis bounds - graph 1
    max_val = data_melt['value'].max()
    if max_val < 1:
        max_val_denom = .1
        max_val_1 = max_val_denom * -(-max_val//max_val_denom)
    else:
        max_val_str = str(min(99, int(max_val))) # In case we have a 100% cca
        first_digit = str(int(max_val_str[0]) + 1)
        num_zero = len(max_val_str) - 1
        max_val_1 = int(first_digit + num_zero * "0")

    # Set y axis bounds - graph 2
    max_val = data2_melt['value'].max()
    max_str = str(int(max_val))
    num_zero = len(max_str) - 1
    first_digit = max_str[0]
    first_digit = str(int(first_digit) + 1)
    max_val_2 = int(first_digit + "0" * num_zero)

    # Bar Graph 1: Primary
    bar = px.bar(
        data_frame=data_melt,
        x = 'Variable',
        y = 'value', 
        barmode='group',
        color='year',
        color_discrete_sequence=[px.colors.qualitative.Safe[0], px.colors.qualitative.Vivid[7], "#00558c"],
        title=f"{title1_label}: 311 Request Response Time Splits",
        labels={    "Variable": "Responsiveness Time",
                    "value": "% Requests Completed",
                    "year": "Year"},
        hover_data={'year': True,
                    'Variable': False,
                    'value': True},
        range_y=[0,max_val_1]
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
        title=f"{title1_label}: {title2_label}",
        labels={    "Variable": f"{title1_label} vs. Chicago Avg.",
                    "value": 'Variable',
                    "year": "Year"},
        hover_data={'year': True,
                    'Variable': False,
                    'value': True},
        range_y=[0,max_val_2]

        )
    bar2.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537", font_color = '#fff')

    return bar, bar2


# Make scatterplot
# Scatter demos : First and second filter
@app.callback(
    dash.dependencies.Output('secondary_scatter', 'options'),
    dash.dependencies.Output('secondary_scatter', 'value'),
    dash.dependencies.Output('secondary_scatter', 'disabled'),
    [dash.dependencies.Input('primary_scatter', 'value')]
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
    dash.dependencies.Output('tertiary_scatter', 'options'),
    dash.dependencies.Output('tertiary_scatter', 'value'),
    dash.dependencies.Output('tertiary_scatter', 'disabled'),
    [dash.dependencies.Input('secondary_scatter', 'value'),
     dash.dependencies.Input('primary_scatter', 'value')]
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


@app.callback(
    Output(component_id = 'scatter', component_property='figure'),
    [Input(component_id = 'scatter_y', component_property='value'),
    Input(component_id = 'primary_scatter', component_property='value'),
    Input(component_id = 'secondary_scatter', component_property='value'),
    Input(component_id = 'tertiary_scatter', component_property='value')]
    )

def update_scatter(scatter_y, overall_filter, demo, secondary_demo):
    '''
    Updates scatter plot based on demo selected
    '''
    if overall_filter == 'Race':
        output_col = df_311_census[demo].copy()
    elif overall_filter == 'Unemployment':
        output_col = df_311_census[demo].copy()
    else:
        potential_incomes = df_311_census[income_cols].copy()
        cols = potential_incomes.columns
        min_idx = cols.get_loc(demo)
        max_idx = cols.get_loc(secondary_demo)
        to_sum = potential_incomes.iloc[:, min_idx: max_idx + 1]
        output_col = to_sum.sum(axis=1)

    # Set up data to output
    demo_output = pd.DataFrame()
    demo_output.loc[:,scatter_y] = df_311_census[scatter_y]
    demo_output.loc[:, 'Population'] = df_311_census['total_num_race_estimates']
    demo_output.loc[:, 'output_col'] = output_col
    demo_output.loc[:, 'cca_name_x'] = df_311_census['cca_name_x']

    # Set up title info and output_col_title
    if overall_filter == 'Race':
        title_label = race_value_to_label[demo]
        output_hover_data = "% " + title_label # Create column name for hover_data
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

    # Set y axis bounds
    max_val = demo_output[scatter_y].max()
    max_str = str(int(max_val))
    num_zero = len(max_str) - 1
    first_digit = max_str[0]
    first_digit = str(int(first_digit) + 1)
    max_val = int(first_digit + "0" * num_zero)

    label_y = dict_scatter_y[scatter_y]

    corr_coef = demo_output[output_hover_data].corr(demo_output[scatter_y])

    fig_scatter = px.scatter(
        demo_output,
        x=output_hover_data,
        y=scatter_y,
        size='Population',
        hover_name='cca_name_x',
        title=f"{label_y} vs. Percent {title_label}",
        labels={'%': f"Percent {title_label}",
                scatter_y: label_y},
        hover_data={output_hover_data: ':.2f',
                    scatter_y: True,
                    'Population': ':,'},  
        range_y=[0, max_val],
        trendline='ols',      
    )
    fig_scatter.add_annotation(x=(max(demo_output[output_hover_data])/2), y=max(demo_output[scatter_y]),
            text=f'Correlation Coefficient: {round(corr_coef, 2)}',
            showarrow=False,
            font=dict(size=18))
    fig_scatter.add_annotation(x=(max(demo_output[output_hover_data])/2), y=max(demo_output[scatter_y])/10*9,
            text=f'<i>Note: Size of bubble corresponds to population of neighborhood</i>',
            showarrow=False,
            font=dict(size=12))
    fig_scatter.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537",
                              font_color = '#fff')

    return fig_scatter


if __name__ == '__main__':
    app.run_server(debug=True)
