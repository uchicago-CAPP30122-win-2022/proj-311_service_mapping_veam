'''
Data pull: Chicago Data Portal (311 Service Requests)

311 Service Mapping Project

File to pull 311 Service Request data for 2019-2021 from Chicago Data Portal
'''

import pandas as pd
from sodapy import Socrata

def retrieve_data():
    '''
    Retreives Chicago 311 Service Request data for 2019-2021 from Chicago Data
        Portal

    Input: None

    Returns (pd.DataFrame): Chicagl 311 data
    '''
    print("Establishing connection with Chicago Data portal...")

    # Data Portal details
    socrata_domain = "data.cityofchicago.org"
    socrata_dataset_identifier = "v6vf-nfxy"
    app_token = "6tRoBirkYQMdr8MMFR8FzgBXq"
    api_username = "v4vigtory@gmail.com"
    api_password = "311_TeamVeam"
    client = Socrata(socrata_domain, app_token,
                    username=api_username,
                    password=api_password)

    print("Pulling 2021 Service Request data from Chicago Data portal")

    # breaking up data collection by year to modularize API pull
    sr_2021 = client.get(socrata_dataset_identifier,
                     select = '''
                        sr_number, sr_type, sr_short_code, 
                        owner_department, status, 
                        created_date, closed_date, 
                        date_extract_y(created_date) as year, 
                        street_address, city, state, zip_code, 
                        community_area, location''',
                     where = '''
                        date_extract_y(created_date) = 2021 AND 
                        community_area IS NOT NULL AND 
                        sr_type NOT IN ('311 INFORMATION ONLY CALL',
                                        'Aircraft Noise Complaint')''',
                     limit = 10000000)

    print("2021 Service Request Data Pull Successful!")

    print("Pulling 2020 Service Request data from Chicago Data portal")

    sr_2020 = client.get(socrata_dataset_identifier,
                     select = '''
                        sr_number, sr_type, sr_short_code, 
                        owner_department, status, 
                        created_date, closed_date, 
                        date_extract_y(created_date) as year, 
                        street_address, city, state, zip_code, 
                        community_area, location''',
                     where = '''
                        date_extract_y(created_date) = 2020 AND 
                        community_area IS NOT NULL AND 
                        sr_type NOT IN ('311 INFORMATION ONLY CALL',
                                        'Aircraft Noise Complaint')''',
                     limit = 10000000)

    print("2020 Service Request Data Pull Successful!")

    print("Pulling 2019 Service Request data from Chicago Data portal")

    sr_2019 = client.get(socrata_dataset_identifier,
                     select = '''
                        sr_number, sr_type, sr_short_code, 
                        owner_department, status, 
                        created_date, closed_date, 
                        date_extract_y(created_date) as year, 
                        street_address, city, state, zip_code, 
                        community_area, location''',
                     where = '''
                        date_extract_y(created_date) = 2019 AND 
                        community_area IS NOT NULL AND 
                        sr_type NOT IN ('311 INFORMATION ONLY CALL',
                                        'Aircraft Noise Complaint')''',
                     limit = 10000000)

    print("2019 Service Request Data Pull Successful!")

    print("Combining data for all 3 years")

    # convert to pandas dataframe
    sr_2021_df = pd.DataFrame(sr_2021)
    sr_2020_df = pd.DataFrame(sr_2020)
    sr_2019_df = pd.DataFrame(sr_2019)

    sr_2019_21_df = pd.concat([sr_2021_df,sr_2020_df,sr_2019_df])

    return sr_2019_21_df
