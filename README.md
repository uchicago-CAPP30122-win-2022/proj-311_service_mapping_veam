# 311 Service Mapping
### CAPP 122 Course Project | Winter 2022
### Team members: Vignesh Venkatachalam, Eujene Yum, Angela The, Matt Kaufmann

Description: Using 311 Service Request information from the Chicago data portal, we will analyze each neighborhood’s “responsiveness” to requests. We will be using 311 data from 2019 to 2021 in order to capture a pre-peak-decline analysis of the pandemic impacts, and will also layer in socio-economic information such as unemployment, income, median rent, and race. Our aim is to understand if there are discernable relationships between a neighborhood's demographic composition and responsiveness, types of issues, and any impact that COVID may have had on these metrics.

### Instructions to view dashboard

All codes to be run from within the `servicemapping` folder

1. To view the dashboard: `python3 -m mapping`
2. To view sample data API-pull from Chicago City Data portal: `python3 -m data_pull.sr311.sr_sample_data_collector`
3. To recreate underlying datasets - by re-pulling Service Request data from Chicago City portal: `python3 -m data_pull.sr311.sr_data_cleaning`
