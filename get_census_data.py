'''
File to take ACS demogrphic data and group into community areas
'''

import censusdata
import pandas as pd
import regex as re
from mapping import create_dictionaries 

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)

tract_cca_d = create_dictionaries()

def go(percentage=False):
    '''
    Runs the files functions to return a df of demos grouped by cca
    
    Input:
        Percentage (boolean): Determines if you get absolute figures vs. % for
            each demographic category
    Returns (pd.DataFrame): Dataframe of demos
    '''
    assert type(percentage) == bool, 'enter True if you want %, False if you want absolute demo values'
    cookbg = get_data_tract_acs()
    cookbg_tracts = parse_geographic_tract_label(cookbg)
    cookbg_filtered = filter_and_groupby_cca(tract_cca_d, cookbg_tracts)
    if not percentage:
        return cookbg_filtered
    return get_percentage_info(cookbg_filtered)


def get_data_tract_acs():
    '''
    Downloads relevant data from american community survey

    Input: None

    Returns (pd.DataFrame): tract level demographics for cook county, IL
    '''
    # Example call from API
    # https://jtleider.github.io/censusdata/example1.html
    
    # Tables used
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B23025'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B19013'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B19001'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'C17002'))
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'B02001'))

    # Alternative for race if needed, but would have to change query
    # censusdata.printtable(censusdata.censustable('acs5', 2015, 'C02003'))
    
    cookbg = censusdata.download('acs5', 2015,
                             censusdata.censusgeo([('state', '17'), ('county', '031'), ('tract', '*')]),
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
    ############# MORE EFFICIENT WAY HERE FOR SURE
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
    filtered_df['cca'] = filtered_df['tract'].map(tract_cca_d)
    return filtered_df.groupby('cca')[cols].sum().reset_index()


def get_percentage_info(df):
    '''
    Creates relevant percentage metrics for each block group

    Input (pd.DataFrame): block group level demographics for cook county, IL

    Returns (pd.DataFrame): Relevant demographics in percentage for use
    '''
    output = pd.DataFrame()
    output['cca'] = df['cca']
    output['percent_unemployed'] = df.unemployed_in_labor_force / df.in_labor_force
    output['LTM_income_sub_10k'] = df.LTM_sub_10k / df.total_num_income_estimates
    output['LTM_income_10-15k'] = df.LTM_10_15k / df.total_num_income_estimates
    output['LTM_income_15_20k'] = df.LTM_15_20k / df.total_num_income_estimates
    output['LTM_income_20_25k'] = df.LTM_20_25k / df.total_num_income_estimates
    output['LTM_income_25_30k'] = df.LTM_25_30k / df.total_num_income_estimates
    output['LTM_income_30_35k'] = df.LTM_30_35k / df.total_num_income_estimates
    output['LTM_income_35_40k'] = df.LTM_35_40k / df.total_num_income_estimates
    output['LTM_income_40_45k'] = df.LTM_40_45k / df.total_num_income_estimates
    output['LTM_income_45_50k'] = df.LTM_45_50k / df.total_num_income_estimates
    output['LTM_income_50_60k'] = df.LTM_50_60k / df.total_num_income_estimates
    output['LTM_income_60_75k'] = df.LTM_60_75k / df.total_num_income_estimates
    output['LTM_income_75_100k'] = df.LTM_75_100k / df.total_num_income_estimates
    output['LTM_income_100_125k'] = df.LTM_100_125k / df.total_num_income_estimates
    output['LTM_income_125_150k'] = df.LTM_125_150k / df.total_num_income_estimates
    output['LTM_income_150_200k'] = df.LTM_150_200k / df.total_num_income_estimates
    output['LTM_income_200k+'] = df['LTM_200k+'] / df.total_num_income_estimates    
    output['below_0.50_poverty_line'] = df['sub_0.50'] / df.total_num_poverty_ratio_estimates
    output['0.50_1.00_poverty_line'] = df['0.50_1.00'] / df.total_num_poverty_ratio_estimates
    output['1.00_1.25_poverty_line'] = df['1.00_1.25'] / df.total_num_poverty_ratio_estimates
    output['1.25_1.50_poverty_line'] = df['1.25_1.50'] / df.total_num_poverty_ratio_estimates
    output['1.50_1.85_poverty_line'] = df['1.50_1.85'] / df.total_num_poverty_ratio_estimates
    output['1.85_2.00_poverty_line'] = df['1.85_2.00'] / df.total_num_poverty_ratio_estimates
    output['2.00+_poverty_line'] = df['2.00+'] / df.total_num_poverty_ratio_estimates
    output['White'] = df.White / df.total_num_race_estimates
    output['Black_or_African_American'] = df.Black_or_African_American / df.total_num_race_estimates
    output['American_Indian_or_Alaska_Native'] = df.American_Indian_or_Alaska_Native / df.total_num_race_estimates
    output['Asian'] = df.Asian / df.total_num_race_estimates
    output['Native_Hawaiian_or_Other_Pacific_Islander'] = df.Native_Hawaiian_or_Other_Pacific_Islander / df.total_num_race_estimates
    output['some_other_race_alone'] = df.some_other_race_alone / df.total_num_race_estimates
    output['two_or_more_races'] = df.two_or_more_races / df.total_num_race_estimates
    return output