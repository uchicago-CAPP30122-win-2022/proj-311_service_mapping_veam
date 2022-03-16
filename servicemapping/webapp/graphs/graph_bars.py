'''
Graph: Bar graphs

311 Service Mapping Project

Create layout for bar graphs (based on Chicago 311 service request data)
'''

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from servicemapping.webapp.inputs.dicts import neighborhood_to_cca_num, neighborhoods, \
    dropdown_style_d, dict_311_stat, dict_responsetime, comm_area_dict
from servicemapping.webapp.inputs.data import service_311_bar, chicago_311_avg
from servicemapping.maindash import app


# -----------------------------------------------------------
# Layout - Core Components + Graph

first_filter_header = "Filter: Neighborhood for Deep Dive on Resolution Times of 311 Requests"
second_filter_header = "Filter: 311 Requests Summary Statistic"

middle_row_content = [
    dbc.Row(html.Br()),
    dbc.Row(html.H3(first_filter_header),style={'text-align': 'center'},
            justify='center'),
    dbc.Row(html.Br()),

    # Responsiveness bar graph
    dbc.Row(
            dcc.Dropdown(id="bar_cca",
                        options =[ {'label': hood,
                                    'value': neighborhood_to_cca_num[hood]}
                                    for hood in neighborhoods],
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
                dcc.Graph(id='bar_graph', figure={},
                          style = {'display': 'inline-block',
                                   'width': '80vh',
                                   'height': '60vh'}),
                justify='center'
                )
        ]),

    # Neighborhood vs. Chicago graph
    dbc.Col([
        dbc.Row(html.H5(second_filter_header),style={'text-align': 'center'},
                justify='center'),
        dbc.Row(
            dcc.Dropdown(id="bar2_311",
                        options =[{'label': v,
                                   'value':k}
                                   for k, v in dict_311_stat.items()],
                        multi = False,
                        value = 'median_resol_time',
                        style = dropdown_style_d
                        ),
                        justify='center'
            ),
        dbc.Row(
            dcc.Graph(id='bar2_graph', figure={},
                       style = {'display': 'inline-block',
                                'width': '80vh', 'height': '60vh'}),
            justify='center'
            )
        ])

    ]


# -----------------------------------------------------------
# App Callback

# Update bar graph
@app.callback(
    [Output(component_id = 'bar_graph', component_property='figure'),
    Output(component_id = 'bar2_graph', component_property='figure')],
    [Input(component_id = 'bar_cca', component_property='value'),
    Input(component_id = 'bar2_311', component_property='value')]
    )

def update_bar(neighborhood, statistic_311):
    '''
    Update bar graph based on dropdown inputs

    Inputs:
        neighborhood (str): Neighborhood to visualize in detail
        statistic_311 (str): 311 statistic to focus 2nd bar graph on

    Returns:
        responsiveness_bar (px.bar): Responsiveness time comparison by year for
            a neighborhood
        neighborhood_v_chicago_bar (px.bar): Chicago avg. vs. neighborhood
            responsivness comparison
    '''

    bar_data_filter = service_311_bar[(
                      service_311_bar['community_area'] == neighborhood)]
    bar_data_filter = bar_data_filter.set_index('year').T.rename_axis(
                                                    'Variable').reset_index()

    # Filter data for main bar graph
    drop1 = ['community_area', 'total_reqs', 'avg_resol_time',
             'median_resol_time', 'sr_per_1000', 'total_num_race_estimates']
    pre_melt = bar_data_filter[~bar_data_filter['Variable'].isin(drop1)]
    data_melt = pd.melt(pre_melt, id_vars=['Variable'], var_name='year',
                        value_name='value')
    data_melt['value'] = round(data_melt['value'] * 100, 2)

    # Filter data for secondary bar graph
    drop2 = list(dict_responsetime.keys())
    drop2.extend([d for d in drop1 if d != statistic_311])
    data2_melt = bar_data_filter[~bar_data_filter['Variable'].isin(drop2)]
    data2_melt = pd.melt(data2_melt, id_vars=['Variable'], var_name='year',
                         value_name='value')

    # Title labels
    title1_label = comm_area_dict[neighborhood]
    title2_label = dict_311_stat[statistic_311]

    # Bring in overall Chicago 311 statistics
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

    # Set bar colors
    bar_colors = [px.colors.qualitative.Safe[0],
                  px.colors.qualitative.Vivid[7],
                  "#00558c"]

    # Bar Graph 1: Responsiveness
    responsiveness_bar = px.bar(
        data_frame=data_melt,
        x = 'Variable',
        y = 'value',
        barmode='group',
        color='year',
        color_discrete_sequence=bar_colors,
        title=f"{title1_label}: 311 Request Response Time Splits",
        labels={    "Variable": "Responsiveness Time",
                    "value": "% Requests Completed",
                    "year": "Year"},
        hover_data={'year': True,
                    'Variable': False,
                    'value': True},
        range_y=[0,max_val_1]
        )
    responsiveness_bar.update_xaxes(
        type='category',
        ticktext = [v for _, v in dict_responsetime.items()],
        tickvals = [k for k, _ in dict_responsetime.items()]
        )
    responsiveness_bar.update_yaxes(
        ticksuffix = "%"
        )
    responsiveness_bar.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537",
                      font_color = '#fff')

    # Bar Graph 2: Neighborhood vs. Chicago
    neighborhood_v_chicago_bar = px.bar(
        data_frame=data2_melt,
        x = 'Variable',
        y = 'value',
        barmode='group',
        color='year',
        color_discrete_sequence=bar_colors,
        title=f"{title1_label}: {title2_label}",
        labels={    "Variable": f"{title1_label} vs. Chicago Avg.",
                    "value": title2_label,
                    "year": "Year"},
        hover_data={'year': True,
                    'Variable': False,
                    'value': True},
        range_y=[0,max_val_2]

        )
    neighborhood_v_chicago_bar.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537",
                      font_color = '#fff')

    return responsiveness_bar, neighborhood_v_chicago_bar
