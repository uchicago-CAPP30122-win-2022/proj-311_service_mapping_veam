# Creating a dictionary that maps census tract to community area (neighborhood)
# and vice versa

# Import statements
# import geopandas as gpd
import pandas as pd
import csv


# Read in data (CSV)
census_tracts_raw = pd.read_csv("UChicago GDrive/CS 122/CS 122 Project/census_tracts_2010.csv", header=0, index="geoid10")
census_tracts = census_tracts.loc[:, ['TRACTCE10', 'COMMAREA']]
# census_tracts_geo = gpd.read_file("UChicago GDrive/CS 122/CS 122 Project/census_tracts_2010.geojson")

# Remove duplciates (even if there aren't any)
assert not census_tracts.duplicated(subset="TRACTCE10").any()

# Make dictionaries for census tract to Chicago Community Area (and vice versa)
tract_cca_dict = {}
cca_tract_dict = {}

for row in census_tracts.iloc:
    tract = row["TRACTCE10"]
    cca = row["COMMAREA"]
    tract_cca_dict[tract] = cca
    cca_tract_dict[cca] = cca_tract_dict.get(cca, []) + [tract]