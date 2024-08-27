import pandas as pd
import os
# from plyer import notification


cleaned_plans = 'cleaned_daywise_plans/'
cleaned_reports = 'Report/'

#Reading the directory
list_of_plans = os.listdir(cleaned_plans)
list_of_reports = os.listdir(cleaned_reports)

for plan in list_of_plans:
    if plan.endswith('.csv'):
        plan_file_path = os.path.join(cleaned_plans, plan)
        df_plan = pd.read_csv(plan_file_path)
        
for report in list_of_reports:
    if report.endswith('.csv'):
        report_file_path = os.path.join(cleaned_reports, report)
        df_report = pd.read_csv(report_file_path)

# df_report['Date'] = pd.to_datetime(df_report['Date'], dayfirst=True)
df_plan['Date'] = pd.to_datetime(df_plan['Date'], format = '%Y-%m-%d')
df_report['Date'] = pd.to_datetime(df_report['Date'], format = '%Y-%m-%d')


# Grouping by Date, Publisher, and Line Item Name and aggregating
aggregated_df_line_item = df_report.groupby(['Date', 'Publisher', 'Line Item Name']).agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Views': 'sum',
    '25% Views': 'sum',
    '50% Views': 'sum',
    '75% Views': 'sum',
    '100% Views': 'sum',
    'Spends': 'sum'
}).reset_index()

# print(aggregated_df)

#Merging the plan and report
df_merged = pd.merge(df_plan, aggregated_df_line_item, left_on=['Date', 'Line_Item'], right_on=['Date', 'Line Item Name'], how='left')

df_merged = df_merged.rename(
    columns={
        'Geo_x': 'Geo', 
        'Publisher_x':'Publisher', 
        'Platform_x':'Platform',
        'Section_x': 'Section',
        'Ad Unit_x': 'Ad Unit',
        'Deal Type_x': 'Deal Type',
        'Targeting_x': 'Targeting',
        'Est Imp': 'Planned Impressions',
        'Est Clicks': 'Planned Clicks',
        'Est Video Views': 'Planned Video Views',
        'Total Net Cost': 'Planned Spends',
        'Impressions' : 'Delivered Impressions',
        'Clicks':'Delivered Clicks',
        'Views':'Delivered Video Views (True Views)',
        'Spends':'Delievered Spends'}
        )

df_merged.columns

df_merged.loc[:,['Campaign Name','Line_Item','Date','Phase/inputs','Genre', 'Demo', 'Geo','Channel', 'Publisher', 'Platform', 'Section','Asset','Ad Unit', 'Deal Type', 'Targeting', 'Planned Impressions','Delivered Impressions','Planned Clicks','Delivered Clicks','Planned Video Views','Delivered Video Views (True Views)','25% Views', '50% Views', '75% Views', '100% Views','Planned Spends','Delievered Spends']].to_csv('merged_plan_report.csv', index=False) 


print('Merged_Plan created successfully!')

# Creating Concept Wise Report
# Grouping by Date, Publisher, and Line Item Name and aggregating
aggregated_df_concept_name = df_report.groupby(['Date', 'Publisher', 'Line Item Name','Concept Name']).agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Views': 'sum',
    '25% Views': 'sum',
    '50% Views': 'sum',
    '75% Views': 'sum',
    '100% Views': 'sum',
    'Spends': 'sum'
}).reset_index()

aggregated_df_concept_name.columns

#Merging the plan and report
df_merged_concept = pd.merge(df_plan, aggregated_df_concept_name, left_on=['Date', 'Line_Item'], right_on=['Date', 'Line Item Name'], how='left')

df_merged_concept = df_merged_concept.rename(
    columns={
        'Geo_x': 'Geo', 
        'Publisher_x':'Publisher', 
        'Platform_x':'Platform',
        'Section_x': 'Section',
        'Ad Unit_x': 'Ad Unit',
        'Deal Type_x': 'Deal Type',
        'Targeting_x': 'Targeting',
        'Est Imp': 'Planned Impressions',
        'Est Clicks': 'Planned Clicks',
        'Est Video Views': 'Planned Video Views',
        'Total Net Cost': 'Planned Spends',
        'Impressions' : 'Delivered Impressions',
        'Clicks':'Delivered Clicks',
        'Views':'Delivered Video Views (True Views)',
        'Spends':'Delievered Spends'}
        )

df_merged_concept = df_merged_concept.groupby(['Campaign Name','Line_Item','Date','Phase/inputs','Genre', 'Demo', 'Geo', 'Channel', 'Publisher', 'Platform', 'Section','Asset','Ad Unit', 'Deal Type', 'Targeting','Concept Name']).agg({
    'Delivered Impressions': 'sum',
    'Delivered Clicks': 'sum',
    'Delivered Video Views (True Views)': 'sum',
    '25% Views': 'sum',
    '50% Views': 'sum',
    '75% Views': 'sum',
    '100% Views': 'sum',
    'Delievered Spends': 'sum'
}).reset_index()

df_merged_concept.loc[:,['Campaign Name','Line_Item','Date','Phase/inputs','Genre', 'Demo', 'Geo', 'Channel', 'Publisher', 'Platform', 'Section','Ad Unit', 'Deal Type', 'Targeting', 'Concept Name' ,'Delivered Impressions','Delivered Clicks','Delivered Video Views (True Views)','25% Views', '50% Views', '75% Views', '100% Views','Delievered Spends']].to_csv('merged_plan_concept_report.csv', index=False)
print('Merged_Plan_Concept created successfully!')