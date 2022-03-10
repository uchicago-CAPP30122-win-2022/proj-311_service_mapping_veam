from sr_data_collector import retrieve_data
from scraping.create_cca_tract_dict import create_dictionaries
import pandas as pd
import numpy as np

_, comm_area_dict = create_dictionaries()
df = retrieve_data()

def create_derived_cols(df):
    # resol_time
    df['diff_mins'] = (pd.to_datetime(df['closed_date']) - pd.to_datetime(df['created_date']))/np.timedelta64(1,'m')

    # time_open_not_resolved
    df['time_open_unresolved'] = np.where((df['diff_mins'].isna()),1, 0)

    df = df[(df.diff_mins > 0) | (df.time_open_unresolved == 1)]

    # time_open_less_than_1_min
    df['time_open_less_than_1_min'] = np.where(df['diff_mins'] < 1, 1, 0)
    # time_open_1_min_1_hr
    df['time_open_1_min_1_hr'] = np.where((df['diff_mins'] >= 1) & (df['diff_mins'] < 60), 1, 0)
    # time_open_1_hr_12_hr
    df['time_open_1_hr_12_hr'] = np.where((df['diff_mins'] >= 60) & (df['diff_mins'] < 60*12), 1, 0)
    # time_open_12_24_hr
    df['time_open_12_24_hr'] = np.where((df['diff_mins'] >= 60*12) & (df['diff_mins'] < 60*24), 1, 0)
    # time_open_1_3_day
    df['time_open_1_3_day'] = np.where((df['diff_mins'] >= 60*24*1) & (df['diff_mins'] < 60*24*3), 1, 0)
    # time_open_3_7_day
    df['time_open_3_7_day'] = np.where((df['diff_mins'] >= 60*24*3) & (df['diff_mins'] < 60*24*7), 1, 0)
    # time_open_7_14_day
    df['time_open_7_14_day'] = np.where((df['diff_mins'] >= 60*24*7) & (df['diff_mins'] < 60*24*14), 1, 0)
    # time_open_14_30_day
    df['time_open_14_30_day'] = np.where((df['diff_mins'] >= 60*24*14) & (df['diff_mins'] < 60*24*30), 1, 0)
    # time_open_1_3_month
    df['time_open_1_3_month'] = np.where((df['diff_mins'] >= 60*24*30*1) & (df['diff_mins'] < 60*24*30*3), 1, 0)
    # time_open_3_12_month
    df['time_open_3_12_month'] = np.where((df['diff_mins'] >= 60*24*30*3) & (df['diff_mins'] < 60*24*30*12), 1, 0)
    # time_open_1_year_plus
    df['time_open_1_year_plus'] = np.where((df['diff_mins'] >= 60*24*30*12),1, 0)
    
    return df

# visual 4
def create_agg_chart_df(df):
    df_viz_4 = df.groupby(["community_area","year"]).agg(
        total_reqs = ("sr_number", len),
        avg_resol_time = ("diff_mins", np.mean),
        median_resol_time = ("diff_mins", np.median),
        perc_resol_less_than_1 = ("time_open_less_than_1_min", np.mean),
        perc_resol_1_min_1_hr = ("time_open_1_min_1_hr", np.mean),
        perc_resol_1_hr_12_hr = ("time_open_1_hr_12_hr", np.mean),
        perc_resol_12_24_hr = ("time_open_12_24_hr", np.mean),
        perc_resol_1_3_day = ("time_open_1_3_day", np.mean),
        perc_resol_3_7_day = ("time_open_3_7_day", np.mean),
        perc_resol_7_14_day = ("time_open_7_14_day", np.mean),
        perc_resol_14_30_day = ("time_open_14_30_day", np.mean),
        perc_resol_1_3_month = ("time_open_1_3_month", np.mean),
        perc_resol_3_12_month = ("time_open_3_12_month", np.mean),
        perc_resol_1_year_plus = ("time_open_1_year_plus", np.mean),
        perc_resol_unresolved = ("time_open_unresolved", np.mean)
        ).sort_values(by=['community_area',"year"], inplace = False)

    # df_viz_4['cca_name'] = df_viz_4['community_area'].map(comm_area_dict)
    
    return df_viz_4


def write_csv(data, filepath):
    '''
    Write CSV for file.

    Inputs:
        # filename (str): the name for the CSV to write
        data (Pandas dataframe: data to turn into CSV
        filepath (str): filepath to save CSV to

    Returns:
        CSV file of dataframe
    '''

    return data.to_csv(filepath)


# visual 2
def create_agg_map_df():
    pass


df_added_cols = create_derived_cols(df)
df_viz_4 = create_agg_chart_df(df_added_cols)