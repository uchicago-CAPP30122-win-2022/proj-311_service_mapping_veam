# Creating a dictionary that maps census tract to community area (neighborhood)

import pandas as pd

def create_dictionaries():
    '''
    Creates a dictionary for Chicago community areas + census tracts
    
    Inputs: None
    
    Returns (dictionary): Tract: community area;
    '''
    # Read in data (CSV)
    census_tracts_raw = pd.read_csv("data/census_tracts_2010.csv", header=0, index_col="GEOID10")
    census_tracts = census_tracts_raw.loc[:, ['TRACTCE10', 'COMMAREA']]

    # Confirm no duplicates (there shouldn't be any)
    assert not census_tracts.duplicated(subset="TRACTCE10").any()

    tract_cca_dict = {}

    for row in census_tracts.iloc:
        tract = row["TRACTCE10"] / 100 #Final two digits are block group
        cca = row["COMMAREA"]
        tract_cca_dict[tract] = cca
    
    return tract_cca_dict