# 311 Service Mapping
## CAPP 122 Course Project | Winter 2022
## Team members: Vignesh Venkatachalam, Eujene Yum, Angela The, Matt Kaufmann

Description: Using 311 Service Request information from the Chicago data portal, we will analyze each neighborhood’s “responsiveness” to requests. We will be using 311 data from 2019 to 2021 in order to capture a pre-peak-decline analysis of the pandemic impacts, and will also layer in socio-economic information such as unemployment, income, median rent, and race. Our aim is to understand if there are discernable relationships between a neighborhood's demographic composition and responsiveness, types of issues, and any impact that COVID may have had on these metrics.

## Instructions to execute project codes

NOTE: All codes to be run from within the `servicemapping` folder

### Setting up Virtual Environment and installing required packages

### Viewing Dashboard
1. Run `python3 -m mapping`
2. Follow the generated URL link

### (Optional) Pulling Data from Chicago Data Portal

#### To view sample data API-pull from Chicago City Data portal: 
1. Run `python3 -m data_pull.sr311.sr_sample_data_collector`
2. Sample dataset created is stored in `data/sr_sample_raw.csv`

#### To recreate underlying datasets - by re-pulling Service Request data from Chicago City portal: (Run Time: ~5 mins)
1. Run `python3 -m data_pull.sr311.sr_data_cleaning`
2. 3 datasets (`311_census_bar.csv`, `sr_census_df` and `chicago_df`) are created and stored in `data/`
