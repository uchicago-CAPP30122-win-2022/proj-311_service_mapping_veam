'''
Inputs: Dictionaries & Lists

311 Service Mapping Project

Create and store dictionaries used for Dash Plotly data visualizations
'''

from servicemapping.data_pull.census.create_cca_tract_dict import create_dictionaries

# -----------------------------------------------------------
# Dictionaries

# Dict: Dropdown style
dropdown_style_d = {'display': 'inline-block',
                    'text-align': 'center',
                    'font-family': 'Helvetica',
                    'color': '#4c9be8',
                    'width': '70%'}

# Dict: Community Area Number ~ Neighborhood Name
_, comm_area_dict = create_dictionaries()
neighborhood_to_cca_num = {v: k for k,v in comm_area_dict.items()}

# List: Chicago Neighborhoods
neighborhoods = []
for neighbordhood in comm_area_dict.values():
    neighborhoods.append(neighbordhood)
neighborhoods = sorted(neighborhoods)

# Lists: Income Dropdowns
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

# Dicts: First map filters, multi-layer drop levels
race_label_to_value = {"White": "White",
                       "Black": "Black_or_African_American",
                       "Native American": "American_Indian_or_Alaska_Native",
                       "Asian": "Asian",
                       "Native Hawaiian / Pacific Islander":
                            "Native_Hawaiian_or_Other_Pacific_Islander",
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
unemployment_value_to_label = {v: k for k, v in unemployment_label_to_value.items()}

second_filter = {
    'Race': race_label_to_value,
    'Range of annual incomes': min_income_label_to_value,
    'Unemployment': unemployment_label_to_value
    }

third_filter = {'Race': {"--": "--"}, 'Unemployment': {"--": "--"}}

# Dict: Second map filter
map_311_filter = {
    "sr_per_1000": "Avg. Annual Num. Service Requests (per 1000 people)",
    "avg_resol_time": "Avg. Resolution Time (days)",
    "median_resol_time": "Median Resolution Time (days)"}

# Dicts: For bar plots
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
    "sr_per_1000": "Annual Num. of 311 Requests (per 1000 people)",
    "avg_resol_time": "Avg. 311 Request Resolution Time (days)",
    "median_resol_time": "Median 311 Request Resolution Time (days)"
    }

# Dicts: For scatter plot
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
