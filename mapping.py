# Creating a dictionary that maps census tract to community area (neighborhood)
# and vice versa

# Import statements
# import geopandas as gpd
import pandas as pd
import csv


# Read in data (CSV)
census_tracts_raw = pd.read_csv("data/census_tracts_2010.csv", header=0, index="geoid10")
census_tracts = census_tracts_raw.loc[:, ['TRACTCE10', 'COMMAREA']]

# Confirm no duplicates (there shouldn't be any)
assert not census_tracts.duplicated(subset="TRACTCE10").any()

# Make dictionaries for census tract to Chicago Community Area (and vice versa)
tract_cca_dict = {}
cca_tract_dict = {}

for row in census_tracts.iloc:
    tract = row["TRACTCE10"]
    cca = row["COMMAREA"]
    tract_cca_dict[tract] = cca
    cca_tract_dict[cca] = cca_tract_dict.get(cca, []) + [tract]