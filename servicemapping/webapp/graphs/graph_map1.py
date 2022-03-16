'''
Graph: Map 1 (Census demographics)

311 Service Mapping Project

Create layout for first map (based on ACS demographics)
'''

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from servicemapping.webapp.inputs.dicts import dropdown_style_d, second_filter, \
    third_filter, income_cols, max_income_tuples, race_value_to_label, \
    unemployment_value_to_label, min_income_value_to_label, \
    max_income_value_to_label
from servicemapping.webapp.inputs.data import census_data, geojson
from servicemapping.maindash import app


# -----------------------------------------------------------
# Layout - Core Components + Graph

demo_map = [
        html.Br(),
        dbc.Row(html.H3("Filter: Neighborhood Census Demographics"),
                style={'text-align': 'center'},justify='center'),
        html.Br(),
        dbc.Row(
            dcc.Dropdown(id="primary_filter",
                         options =[
                            {"label": "Race", "value": "Race"},
                            {"label": "Range of annual incomes",
                             "value": "Range of annual incomes"},
                            {"label": "Percent unemployed",
                             "value": "Unemployment"}],
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
            dcc.Graph(id='demo_map',
                      figure={'layout': {'paper_bgcolor': "#0f2537",
                                         'plot_bgcolor': "#0f2537"}},
                      style = {'display': 'inline-block', 'width': '80vh',
                               'height': '80vh'},
                      ),
            justify='center'
            )
    ]


# -----------------------------------------------------------
# App Callbacks

# Set second filter options (if applicable)
@app.callback(
    dash.dependencies.Output('secondary_filter', 'options'),
    dash.dependencies.Output('secondary_filter', 'value'),
    dash.dependencies.Output('secondary_filter', 'disabled'),
    [dash.dependencies.Input('primary_filter', 'value')]
    )

def set_second_options_and_value(option):
    '''
    Updates secondary filter options

    Input:
        option (str): Primary demographic filter (race / income / unemployment)

    Returns: 3 dash dropdown components for secondary filter:
        1) options (ddc component): Filter options
        2) value (ddc component): Default value
        3) diabled (ddc component): Whether or not you can change the filter
    '''
    options = [{'label': k,
                'value': v} for k,v in second_filter[option].items()]
    disabled = False
    if option == 'Unemployment':
        disabled = True
    return options, options[0]['value'], disabled


# Set third filter options (if applicable)
@app.callback(
    dash.dependencies.Output('tertiary_filter', 'options'),
    dash.dependencies.Output('tertiary_filter', 'value'),
    dash.dependencies.Output('tertiary_filter', 'disabled'),
    [dash.dependencies.Input('primary_filter', 'value'),
     dash.dependencies.Input('secondary_filter', 'value')]
    )

def set_third_options(first_filter, option):
    '''
    Updates third filter options

    Inputs:
        first_filter (str): Primary demographic filter (race / income /
            unemployment)
        option (str): Secondary demographic filter (type of race /
            min income level)

    Returns: 3 dash dropdown components for tertiary filter:
        1) options (ddc component): Filter options
        2) value (ddc component): Default value
        3) diabled (ddc component): Whether or not you can change the filter
    '''
    if first_filter != 'Range of annual incomes':
        options =  [{'label': k,
                     'value': v} for k,v in third_filter[first_filter].items()]
        disabled = True
    else:
        idx = income_cols.index(option)
        options =  [{'label': l,
                     'value': v} for l,v in max_income_tuples[idx:]]
        disabled = False
    return options, options[0]['value'], disabled


# Update map (Census demographics)
@app.callback(
    Output(component_id = 'demo_map', component_property='figure'),
    [Input(component_id = 'primary_filter', component_property='value'),
    Input(component_id = 'secondary_filter', component_property='value'),
    Input(component_id = 'tertiary_filter', component_property='value')]
    )

def update_census_map(overall_filter, demo, secondary_demo):
    '''
    Updates census graph based on demographic information

    Inputs:
        overall_filter (str): Primary demographic filter (race / income /
            unemployment)
        demo (str): Secondary demographic filter (type of race /
            min income level)
        secondary_demo (str): Max income level (if applicable)

    Returns:
        census_demo_map(px.choropleth_mapbox): Chicago demographic mapped by
            neighborhood
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
        output_hover_data = "% " + title_label
        demo_output[output_hover_data] = demo_output['output_col']
    elif overall_filter == 'Unemployment':
        title_label = unemployment_value_to_label[demo]
        output_hover_data = '% Unemp.'
        demo_output[output_hover_data] = demo_output['output_col']
    else:
        min_label = min_income_value_to_label[demo]
        max_label = max_income_value_to_label[secondary_demo]
        if max_label == "No max":
            title_label = "making over " + min_label + " per year"
            output_hover_data = '% >' + min_label
            demo_output[output_hover_data] = demo_output['output_col']
        else:
            title_label = "making between " + min_label + " - " + \
                max_label + " per year"
            output_hover_data = "% b/t " + min_label + " - " + max_label
            demo_output[output_hover_data] = demo_output['output_col']

    # Set the actual output reference column
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

    # Specify demo map figure
    census_demo_map = px.choropleth_mapbox(
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
        title=f"% {title_label}"
    )
    census_demo_map.update_geos(fitbounds='locations', visible=False)
    census_demo_map.update_layout(paper_bgcolor="#0f2537", font_color = '#fff')

    return census_demo_map
