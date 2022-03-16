'''
Inputs: Data

311 Service Mapping Project

Clean and store datasets for Dash Plotly data visualization
'''

import pandas as pd
import geopandas as gpd
import os.path as path

absolute_path_dir = path.abspath(path.join(__file__ ,"../../.."))

# -----------------------------------------------------------
# Import and clean data

# census_data (Used for: graph_map1)
census_data = pd.read_csv(absolute_path_dir + "/data/census_demos.csv")
census_data["cca_num"] = census_data["cca_num"].astype(str)

# geojson (Used for: graph_map1 and graph_map2)
geojson = gpd.read_file(absolute_path_dir + "/data/community_areas.geojson")

# chicago_311_avg (Used for: graph_bars)
chicago_311_avg = pd.read_csv(absolute_path_dir + "/data/chicago_df.csv")

# df_311_census (Used for: graph_map2 and graph_scatter)
df_311_census = pd.read_csv(absolute_path_dir + "/data/sr_census_df.csv")

# service_311_bar (Used for: graph_bars)
service_311_bar = pd.read_csv(absolute_path_dir + "/data/311_census_bar.csv")
to_use_to_make_per_1k = df_311_census[['cca_num_x', 'total_num_race_estimates']]
service_311_bar = service_311_bar.merge(to_use_to_make_per_1k,
                                        left_on="community_area",
                                        right_on="cca_num_x")
del service_311_bar["cca_num_x"]
service_311_bar['sr_per_1000'] = 1000 * (service_311_bar['total_reqs'] /
                                 service_311_bar['total_num_race_estimates'])


# -----------------------------------------------------------
# Data Cleaning (for visualization)

# Change percent resolutions unresolved to percentage points vs. decimal
# e.g. to 9.70 from .097
df_311_census['perc_resol_unresolved'] = df_311_census['perc_resol_unresolved'] * 100

# Round data off
for df in [service_311_bar, df_311_census]:
    df['avg_resol_time'] = df['avg_resol_time']/(24*60)
    df['avg_resol_time'] = df['avg_resol_time'].round(2)
    df['median_resol_time'] = df['median_resol_time']/(24*60)
    df['median_resol_time'] = df['median_resol_time'].round(2)
    df['sr_per_1000'] = df['sr_per_1000'].round(0)
    df_311_census['perc_resol_unresolved'] = df_311_census['perc_resol_unresolved'].round(2)

# Rename top 311 issue column titles
df_311_census['Top 311 issue'] = df_311_census['top_1']
df_311_census['2nd issue'] = df_311_census['top_2']
df_311_census['3rd issue'] = df_311_census['top_3']

# Make service request per 1000 on annual basis vs. 3 year total
df_311_census['sr_per_1000'] = df_311_census['sr_per_1000'] // 3
