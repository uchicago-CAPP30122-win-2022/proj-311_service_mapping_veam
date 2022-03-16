'''
Graph: Scatterplot

311 Service Mapping Project

Create layout for scatterplot based on ACS demographics & Chicago 311 service
    request data
'''

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import statsmodels

from servicemapping.webapp.inputs.dicts import dropdown_style_d, dict_scatter_y, \
    second_filter, third_filter, income_cols, max_income_tuples, \
    race_value_to_label, unemployment_value_to_label, \
    min_income_value_to_label, max_income_value_to_label
from servicemapping.webapp.inputs.data import df_311_census
from servicemapping.maindash import app


# -----------------------------------------------------------
# Layout - Core Components + Graph
# Bottom row - scatterplot

filter_header = "Filter: Plotting Census Demographics on 311 Service Request Data"

bottom_row_content = [
    dbc.Row(html.Br()),
    dbc.Row(html.Br()),
    dbc.Row(html.H3(filter_header),style={'text-align': 'center'},
                    justify='center'),
    dbc.Row(html.Br()),

    dbc.Row([
        dbc.Col([
            dbc.Row(html.H5("Select a Census Demographic (X Var)"),
                    style={'text-align': 'center'},justify='center'),
            dbc.Row(
            dcc.Dropdown(id="primary_scatter",
                         options =[
                            {"label": "Race",
                             "value": "Race"},
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
            dbc.Row(html.H5("Select 311 info (Y Var)"),
                    style={'text-align': 'center'},justify='center'),
            dbc.Row(
                dcc.Dropdown(id="scatter_y",
                    options =[ {'label': v,
                                'value': k}
                                for k, v in dict_scatter_y.items()],
                    multi = False,
                    value = "median_resol_time",
                    style = dropdown_style_d
                    ),
                justify='center')
            ]),
    ]),
    dbc.Row(
        dcc.Graph(id='scatter',
                  figure={'layout': {'paper_bgcolor': "#0f2537",
                          'plot_bgcolor': "#0f2537"}},
            style = {'display': 'inline-block',
                     'width': '100vh', 'height': '80vh'}),
            justify='center'
        ),
    dbc.Row(html.Br())
    ]


# -----------------------------------------------------------
# App Callbacks
# Update scatterplot

# Set second filter options (if applicable)
@app.callback(
    dash.dependencies.Output('secondary_scatter', 'options'),
    dash.dependencies.Output('secondary_scatter', 'value'),
    dash.dependencies.Output('secondary_scatter', 'disabled'),
    [dash.dependencies.Input('primary_scatter', 'value')]
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
    options = [{'label': k, 'value': v} for k,v in second_filter[option].items()]
    disabled = False
    if option == 'Unemployment':
        disabled = True
    return options, options[0]['value'], disabled

# Set third filter options (if applicable)
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
        options =  [{'label': k, 'value': v} for k,v in third_filter[first_filter].items()]
        disabled = True
    else:
        idx = income_cols.index(option)
        options =  [{'label': l, 'value': v} for l,v in max_income_tuples[idx:]]
        disabled = False
    return options, options[0]['value'], disabled

# Update scatterplot
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

    Inputs:
        scatter_y (str): 311 data to use as target for correlation
        overall_filter (str): Primary demographic filter (race / income /
            unemployment)
        demo (str): Secondary demographic filter (type of race /
            min income level)
        secondary_demo (str): Max income level (if applicable)

    Returns:
        fig_scatter(px.scatter): Scatterplot of 311 info vs. demo info for
            Chicago neighborhoods
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
            title_label = "making between " + min_label + " - " + max_label + " per year"
            output_hover_data = "% b/t " + min_label + " - " + max_label
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

    # Set position of scatterplot annotations
    x_max = max(demo_output[output_hover_data])
    x_min = min(demo_output[output_hover_data])

    corr_coef = demo_output[output_hover_data].corr(demo_output[scatter_y])

    # Specify scatterplot figure
    fig_scatter = px.scatter(
        demo_output,
        x=output_hover_data,
        y=scatter_y,
        size='Population',
        hover_name='cca_name_x',
        title=f"{label_y} vs. Percent {title_label}",
        labels={'%': f"Percent {title_label}",
                scatter_y: label_y},
        trendline='ols',
        trendline_color_override=px.colors.qualitative.Vivid[7],
        hover_data={output_hover_data: ':.2f',
                    scatter_y: True,
                    'Population': ':,'},
        range_y=[0, max_val],
    )

    fig_scatter.add_annotation(x=((x_max + x_min)/2), y=max_val,
            text=f'Correlation Coefficient: {round(corr_coef, 2)}',
            showarrow=False,
            font=dict(size=18))
    note = "Note: Size of bubble corresponds to population of neighborhood"
    fig_scatter.add_annotation(x=((x_max + x_min)/2), y=max_val/20*19,
            text=f'<i>{note}</i>',
            showarrow=False,
            font=dict(size=12))
    fig_scatter.update_layout(paper_bgcolor="#0f2537", plot_bgcolor="#0f2537",
                              font_color = '#fff')
    fig_scatter.update_traces(marker_color=px.colors.qualitative.Vivid[7])

    return fig_scatter
