'''
File to clean 311 Service Request Data to make it available for Dash visualizations
'''

from sr_data_collector import retrieve_data
import pandas as pd
import numpy as np

census_pop_data = pd.read_csv("data/census_demos_pop.csv")
census_demo_data = pd.read_csv("data/census_demos.csv")

def get_data():
    df = retrieve_data()
    return df

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

# visual 4 (bar graph by year)
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
                 
    return df_viz_4


# visual 2 and 3 (map & scatter plot)
def create_sr_census_df(df, census_pop_data, census_demo_data):
    # create top_sr_pivot_final
    # create filtered df for top 8 SR types
    df_filtered = df[df.sr_type.isin(['Graffiti Removal Request','Street Light Out Complaint','Rodent Baiting/Rat Complaint','Pothole in Street Complaint','Garbage Cart Maintenance','Weed Removal Request','Tree Trim Request','Abandoned Vehicle Complaint'])]

    df_filtered = df_filtered.groupby(["community_area", 'sr_type']).agg(
        sr_type_count = ('sr_number', len))
    
    # creating actual pivot for top 8 SR types
    top_sr_pivot = pd.pivot_table(df_filtered, 
                       values='sr_type_count', 
                       index='community_area', 
                       columns='sr_type', 
                       aggfunc=np.mean)
    top_sr_final = top_sr_pivot.reset_index()
    top_sr_final['community_area'] = top_sr_final['community_area'].astype(int)

    # create sr_pivot (top 3 SR by community area)
    df_top = df[['community_area', 'sr_number', 'sr_type']]
    
    df_top_all_sr = df_top.groupby(["community_area", "sr_type"]).agg(total_reqs = ("sr_number", len)).sort_values(by=['community_area','total_reqs'], ascending = [True, False], inplace = False)
    
    df_top_3_sr = df_top_all_sr.groupby(["community_area"]).head(3).reset_index()
    
    df_top_3_sr["sr_type_rank"] = df_top_3_sr.groupby('community_area')['total_reqs'].rank(ascending=False).astype(int)

    sr_pivot = pd.pivot_table(df_top_3_sr, 
                       values='sr_type', 
                       index='community_area', 
                       columns='sr_type_rank', 
                       aggfunc=lambda x: ' '.join(x))
    sr_pivot = sr_pivot.rename(columns={1: "top_1", 2: "top_2",3:"top_3"})
    sr_pivot = sr_pivot.reset_index()
    sr_pivot['community_area'] = sr_pivot['community_area'].astype(int)

    # create SR_DF (aggregated 311 data)
    sr_df = df.groupby(["community_area"]).agg(
        total_reqs = ("sr_number", len),
        avg_resol_time = ("diff_mins",np.mean),
        median_resol_time = ("diff_mins", np.median),
        perc_resol_unresolved = ("time_open_unresolved", np.mean)
        ).sort_values(by=['community_area'], inplace = False)
    
    sr_df = sr_df.reset_index()
    sr_df['community_area'] = sr_df['community_area'].astype(int)

    # add in total population(from census_demo_pop) and census_demo columns
    sr_pop_df = pd.merge(sr_df, 
                   census_pop_data[['cca_num','cca_name','total_num_race_estimates']], 
                   left_on ='community_area',
                   right_on='cca_num',
                   how='left')
    # add calculated column
    sr_pop_df["sr_per_1000"] = sr_pop_df.total_reqs / sr_pop_df.total_num_race_estimates * 1000
    
    sr_pop_demo_df = pd.merge(sr_pop_df, 
                   census_demo_data, 
                   left_on ='community_area',
                   right_on='cca_num',
                   how='left'
                  )
    sr_pop_demo_topsr_df = pd.merge(sr_pop_demo_df,
                       top_sr_final,
                       left_on ='community_area',
                        right_on='community_area',
                        how='left'
                  )
    sr_census_df = pd.merge(sr_pop_demo_topsr_df, 
                   sr_pivot, 
                   left_on ='community_area',
                   right_on='community_area',
                   how='left'
                  )
    sr_census_df = sr_census_df.rename(columns={'cca_name_y': "cca_name"})
    #drop_lst = ['cca_num_x', 'cca_name_x','cca_num_y','index_x','level_0_x','index_y','level_0_y','index']
    #sr_census_df = sr_census_df.drop(drop_lst, axis=1)

    return sr_census_df

def create_static_df(df,census_pop_data):
    chicago = {'City': ["Chicago"]}
    chicago_df = pd.DataFrame(data=chicago)

    total_req = len(df)
    avg_res_time = df["diff_mins"].mean()
    median_res_time = df["diff_mins"].median()
    total_pop = census_pop_data['total_num_race_estimates'].sum()

    chicago_df['total_req'] = total_req
    chicago_df['avg_res_time'] = avg_res_time
    chicago_df['median_res_time'] = median_res_time
    chicago_df['sr_per_1000'] = chicago_df.total_req / total_pop *1000

    return chicago_df



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


# if __name__ == '__main__':
#     df_added_cols = create_derived_cols(df)
#     df_viz_4 = create_agg_chart_df(df_added_cols)
#     write_csv(df_viz_4, 'data/df_viz_4.csv')
#     #sr_census_df = create_sr_census_df(df, census_pop_data, census_demo_data)
#     #write_csv(sr_census_df, 'data/sr_census_df.csv')
#     chicago_df = create_static_df(df,census_pop_data)
#     write_csv(chicago_df, 'data/chicago_df.csv')