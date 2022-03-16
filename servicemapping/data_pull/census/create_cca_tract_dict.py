'''
Data pull: Census

311 Service Mapping Project

Creates a dictionary that maps census tract to community area (neighborhood)
'''
import pandas as pd
import os.path as path

absolute_path_dir = path.abspath(path.join(__file__ ,"../../.."))

def create_dictionaries():
    '''
    Creates a dictionary for (i) Chicago community areas + census tracts
                             (ii) CCA number to name

    Inputs: None

    Returns (dictionary): Tract: community area;
    '''
    # Read in data (CSV)
    census_tracts_raw = pd.read_csv(absolute_path_dir + "/data/census_tracts_2010.csv", header=0, index_col="GEOID10")
    census_tracts = census_tracts_raw.loc[:, ['TRACTCE10', 'COMMAREA']]

    comm_area_raw = pd.read_csv(absolute_path_dir + "/data/CommAreas.csv", header=0)
    comm_area = comm_area_raw.loc[:, ['AREA_NUM_1', 'COMMUNITY']]

    # Confirm no duplicates (there shouldn't be any)
    assert not census_tracts.duplicated(subset="TRACTCE10").any()

    tract_cca_dict = {}

    for row in census_tracts.iloc:
        tract = row["TRACTCE10"] / 100 #Final two digits are block group
        cca = row["COMMAREA"]
        tract_cca_dict[tract] = cca

    comm_area_dict = {}

    for row in comm_area.iloc:
        cca = row["COMMUNITY"].title()
        cca_num = int(row["AREA_NUM_1"])
        comm_area_dict[cca_num] = cca

    return tract_cca_dict, comm_area_dict
