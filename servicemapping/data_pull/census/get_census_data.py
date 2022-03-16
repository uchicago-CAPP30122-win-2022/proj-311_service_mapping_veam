'''
Data pull: Census

311 Service Mapping Project

File to take ACS demogrphic data and group into community areas
'''

import censusdata
import pandas as pd
import regex as re
import os.path as path
from create_cca_tract_dict import create_dictionaries

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)

absolute_path_dir = path.abspath(path.join(__file__ ,"../../.."))

tract_cca_d, comm_area_dict = create_dictionaries()

default_path = absolute_path_dir + "/data/census_demos.csv"

def go(filepath=default_path, percentage=True):
    '''
    Runs the files functions to return a df of demos grouped by cca

    Input:
        filepath (filepath): Where to save csv
        percentage (boolean): Determines if you get absolute figures vs. % for
            each demographic category
    Returns (csv): csv of demos
    '''
    assert isinstance(percentage, bool),\
        'enter True if you want %, False if you want absolute demo values'

    cookbg = get_data_tract_acs()
    cookbg_tracts = parse_geographic_tract_label(cookbg)
    cookbg_filtered = filter_and_groupby_cca(tract_cca_d, cookbg_tracts)
    if percentage:
        cookbg_filtered = get_percentage_info(cookbg_filtered)
    cookbg_filtered['cca_name'] = cookbg_filtered['cca_num'].map(comm_area_dict)
    names = cookbg_filtered.pop('cca_name')
    cookbg_filtered.insert(0, 'cca_name', names)
    return cookbg_filtered.to_csv(filepath)

def get_data_tract_acs():
    '''
    Downloads relevant data from american community survey

    Input: None

    Returns (pd.DataFrame): tract level demographics for cook county, IL
    '''
    # Tables used detail (prints out columns available with titles)
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B23025'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B19013'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B19001'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'C17002'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B02001'))

    cookbg = censusdata.download('acs5', 2015,
                        censusdata.censusgeo([
                            ('state', '17'),
                            ('county', '031'),
                            ('tract', '*')
                            ]),
                            ['B23025_003E', 'B23025_005E',
                            'B19001_001E', 'B19001_002E', 'B19001_003E',
                            'B19001_004E', 'B19001_005E', 'B19001_006E',
                            'B19001_007E', 'B19001_008E', 'B19001_009E',
                            'B19001_010E', 'B19001_011E', 'B19001_012E',
                            'B19001_013E', 'B19001_014E', 'B19001_015E',
                            'B19001_016E', 'B19001_017E', 'C17002_001E',
                            'C17002_002E', 'C17002_003E', 'C17002_004E',
                            'C17002_005E', 'C17002_006E', 'C17002_007E',
                            'C17002_008E', 'B02001_001E', 'B02001_002E',
                            'B02001_003E', 'B02001_004E', 'B02001_005E',
                            'B02001_006E', 'B02001_007E', 'B02001_008E'])
    cookbg.columns = ['in_labor_force', 'unemployed_in_labor_force',
                     'total_num_income_estimates', 'LTM_sub_10k', 'LTM_10_15k',
                     'LTM_15_20k', 'LTM_20_25k', 'LTM_25_30k', 'LTM_30_35k',
                     'LTM_35_40k', 'LTM_40_45k', 'LTM_45_50k', 'LTM_50_60k',
                     'LTM_60_75k', 'LTM_75_100k', 'LTM_100_125k',
                     'LTM_125_150k', 'LTM_150_200k', 'LTM_200k+',
                     'total_num_poverty_ratio_estimates', 'sub_0.50',
                     '0.50_1.00', '1.00_1.25', '1.25_1.50', '1.50_1.85',
                     '1.85_2.00', '2.00+', 'total_num_race_estimates', 'White',
                     'Black_or_African_American',
                     'American_Indian_or_Alaska_Native', 'Asian',
                     'Native_Hawaiian_or_Other_Pacific_Islander',
                     'some_other_race_alone', 'two_or_more_races']
    return cookbg


def parse_geographic_tract_label(df):
    '''
    Parses a geographic label from census data and reindexes df

    Input (pd.DataFrame): block group level demographics for cook county, IL

    Returns (pd.DataFrame): Demos with new columns for census tract
    '''
    output = df.copy()
    labels = df.index
    tracts = []
    for label in labels:
        label = str(label)
        tract = re.findall('Census Tract ([0-9]+.[0-9]+)', label)
        tract = tract[0]
        if "." in tract:
            tracts.append(float(tract))
        else:
            tracts.append(int(tract))
    output['tract'] = tracts
    return output


def filter_and_groupby_cca(tract_d, df):
    '''
    Filters out tracts to only those we want

    Inputs:
        tract_d (dict): dictionary containing tract: cca pairings
        df (pd.DataFrame): block group level demographics for cook county, IL
        filter_on

    Returns (pd.DataFrame): Demos filtered by tract with new col for cca
    '''
    tracts = set()
    for tract in tract_d:
        tracts.add(tract)
    filtered_df = df[(df['tract'].isin(tracts))].copy()
    cols = filtered_df.columns
    cols = cols[:-1] # Remove tract from columns we want to utilize
    filtered_df['cca_num'] = filtered_df['tract'].map(tract_cca_d)
    return filtered_df.groupby('cca_num')[cols].sum().reset_index()


def get_percentage_info(df):
    '''
    Creates relevant percentage metrics for each block group

    Input (pd.DataFrame): block group level demographics for cook county, IL

    Returns (pd.DataFrame): Relevant demographics in percentage for use
    '''
    output = pd.DataFrame()
    output['cca_num'] = df['cca_num']
    output['percent_unemployed'] = (
        df.unemployed_in_labor_force / df.in_labor_force * 100)
    output['LTM_income_sub_10k'] = (
        df.LTM_sub_10k / df.total_num_income_estimates * 100)
    output['LTM_income_10-15k'] = (
        df.LTM_10_15k / df.total_num_income_estimates * 100)
    output['LTM_income_15_20k'] = (
        df.LTM_15_20k / df.total_num_income_estimates * 100)
    output['LTM_income_20_25k'] = (
        df.LTM_20_25k / df.total_num_income_estimates * 100)
    output['LTM_income_25_30k'] = (
        df.LTM_25_30k / df.total_num_income_estimates * 100)
    output['LTM_income_30_35k'] = (
        df.LTM_30_35k / df.total_num_income_estimates * 100)
    output['LTM_income_35_40k'] = (
        df.LTM_35_40k / df.total_num_income_estimates * 100)
    output['LTM_income_40_45k'] = (
        df.LTM_40_45k / df.total_num_income_estimates * 100)
    output['LTM_income_45_50k'] = (
        df.LTM_45_50k / df.total_num_income_estimates * 100)
    output['LTM_income_50_60k'] = (
        df.LTM_50_60k / df.total_num_income_estimates * 100)
    output['LTM_income_60_75k'] = (
        df.LTM_60_75k / df.total_num_income_estimates * 100)
    output['LTM_income_75_100k'] = (
        df.LTM_75_100k / df.total_num_income_estimates * 100)
    output['LTM_income_100_125k'] = (
        df.LTM_100_125k / df.total_num_income_estimates * 100)
    output['LTM_income_125_150k'] = (
        df.LTM_125_150k / df.total_num_income_estimates * 100)
    output['LTM_income_150_200k'] = (
        df.LTM_150_200k / df.total_num_income_estimates * 100)
    output['LTM_income_200k+'] = (
        df['LTM_200k+'] / df.total_num_income_estimates * 100)
    output['below_0.50_poverty_line'] = (
        df['sub_0.50'] / df.total_num_poverty_ratio_estimates * 100)
    output['0.50_1.00_poverty_line'] = (
        df['0.50_1.00'] / df.total_num_poverty_ratio_estimates * 100)
    output['1.00_1.25_poverty_line'] = (
        df['1.00_1.25'] / df.total_num_poverty_ratio_estimates * 100)
    output['1.25_1.50_poverty_line'] = (
        df['1.25_1.50'] / df.total_num_poverty_ratio_estimates * 100)
    output['1.50_1.85_poverty_line'] = (
        df['1.50_1.85'] / df.total_num_poverty_ratio_estimates * 100)
    output['1.85_2.00_poverty_line'] = (
        df['1.85_2.00'] / df.total_num_poverty_ratio_estimates * 100)
    output['2.00+_poverty_line'] = (
        df['2.00+'] / df.total_num_poverty_ratio_estimates * 100)
    output['White'] = (
        df.White / df.total_num_race_estimates * 100)
    output['Black_or_African_American'] = (
        df.Black_or_African_American / df.total_num_race_estimates * 100)
    output['American_Indian_or_Alaska_Native'] = (
        df.American_Indian_or_Alaska_Native / df.total_num_race_estimates * 100)
    output['Asian'] = (
        df.Asian / df.total_num_race_estimates * 100)
    output['Native_Hawaiian_or_Other_Pacific_Islander'] = (
        df.Native_Hawaiian_or_Other_Pacific_Islander / df.total_num_race_estimates * 100)
    output['some_other_race_alone'] = (
        df.some_other_race_alone / df.total_num_race_estimates * 100)
    output['two_or_more_races'] = (
        df.two_or_more_races / df.total_num_race_estimates * 100)
    output['cca_num'].astype(int)
    return output

if __name__ == '__main__':
    go(filepath=default_path, percentage=True)
    print(default_path, "updated")
