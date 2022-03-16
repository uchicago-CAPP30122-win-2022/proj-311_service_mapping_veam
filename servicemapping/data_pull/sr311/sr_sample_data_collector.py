'''
Data pull: Chicago Data Portal (311 Service Requests)

311 Service Mapping Project

File to pull sample 311 Service Request data for Dec 2020 from Chicago Data
    Portal and clean it to produce a sample dataset for data visualization
'''

import pandas as pd
from sodapy import Socrata

def retrieve_data():
    '''
    Retreives sample of Chicago 311 Service Request data from Chicago Data
        Portal

    Input: None

    Returns (pd.DataFrame): Chicagl 311 data sample
    '''

    # Data Portal details
    socrata_domain = "data.cityofchicago.org"
    socrata_dataset_identifier = "v6vf-nfxy"
    app_token = "6tRoBirkYQMdr8MMFR8FzgBXq"
    api_username = "v4vigtory@gmail.com"
    api_password = "311_TeamVeam"
    client = Socrata(socrata_domain, app_token, username=api_username, password=api_password)

    print("Establishing connection with Chicago Data portal...")

    sr_sample = client.get(socrata_dataset_identifier,
                     select = '''sr_number, sr_type, sr_short_code,
                                owner_department, status, 
                                created_date, closed_date, 
                                date_extract_y(created_date) as year, 
                                street_address, city, state, zip_code, 
                                community_area, location''',
                     where = '''date_extract_y(created_date) = 2020 AND 
                                date_extract_m(created_date) = 12 AND 
                                community_area IS NOT NULL AND 
                                sr_type NOT IN ('311 INFORMATION ONLY CALL',
                                                'Aircraft Noise Complaint')''')

    print("Pulling Service Request data from Chicago Data portal using Socrata...")

    # convert to pandas dataframe
    sr_sample_df = pd.DataFrame(sr_sample)

    print("API data-pull Successful! You can find the data under servicemapping/data/sr_sample_raw.csv")

    return sr_sample_df.to_csv("servicemapping/data/sr_sample_raw.csv")

if __name__ == '__main__':
    retrieve_data()
