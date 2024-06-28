import pandas as pd
import os

cleaned_daywise_plans_path = 'cleaned_daywise_plans/'
geo_csv_path = 'geo_csv/'

#Reading the directory
list_of_files = os.listdir(cleaned_daywise_plans_path)

#Reading the first file
for file in list_of_files:
    global campaign_name
    campaign_name = file.split('_')[0] + '_' + file.split('_')[1]
    df_plan = pd.read_csv(cleaned_daywise_plans_path + file)

df_geo = pd.DataFrame(columns = ['Geo'])
df_geo['Geo'] = df_plan['Geo/Cluster'].unique()

df_geo.to_csv(geo_csv_path + campaign_name + '_geo.csv', index=False)