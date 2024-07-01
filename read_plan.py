import pandas as pd
import os

plans_path = 'raw_plans/'
sheet_name = 'Media Plan Phase 1'
overall_plans_path = 'cleaned_plans/'
daywise_plans_path = 'cleaned_daywise_plans/'

#Reading the directory
list_of_files = os.listdir(plans_path)

#Reading the first file
for file in list_of_files:
    global campaign_name
    if file.endswith('.xlsx'):
        plan_file_path = os.path.join(plans_path, file) 
        campaign_name = file.split('_')[0] + '_' + file.split('_')[1]
    elif file.endswith('.csv'):
        plan_file_path = os.path.join(plans_path, file)
        campaign_name = file.split('_')[0] + '_' + file.split('_')[1]
    elif file == 'Done':
        continue

#Plan excel to df
df_plan_excel = pd.ExcelFile(plan_file_path)

#Reading the plan sheet
df_plan = pd.read_excel(df_plan_excel, sheet_name)

#Cleaning the plan
#Dropping rows with no Deal Type
df_plan = df_plan.dropna(subset=['Deal Type'])
df_plan = df_plan.dropna(axis=1, how='all')

columns_to_rename = {
    'Est Imp': ['Est-Imp', 'Est. Imp'],
    'Est Clicks': ['Est-Clicks', 'Est. Clicks', 'Est Clicks'],
    'Est Video Views': ['Est Video Views', 'Views', 'Est Views / Engag'],
    'Total Net Cost': ['Total Net Cost', 'Net Cost']
}

# Standardizing the column names
for standardized_name, column_variants in columns_to_rename.items():
    found = False
    for column in column_variants:
        if column in df_plan.columns:
            df_plan.rename(columns={column: standardized_name}, inplace=True)
            found = True
            break
    if not found:
        print(f'{standardized_name} column not found')


#Ensuring Start Date and End Date are in datetime format
df_plan['Start Date'] = pd.to_datetime(df_plan['Start Date'])
df_plan['End Date'] = pd.to_datetime(df_plan['End Date'])

#Calculating days
df_plan['Total_Days'] = (df_plan['End Date'] - df_plan['Start Date']).dt.days + 1

df_plan['Campaign Name'] = campaign_name
df_plan['Phase/inputs'] = sheet_name

# Exploding the plan daywise
df_plan_daywise = df_plan.reindex(df_plan.index.repeat(df_plan['Total_Days'])).reset_index(drop=True)


# Dividing main Metrics to daywise columns(Impressions, Clicks, Net Cost, Video Views)
for index, row in df_plan_daywise.iterrows():
    df_plan_daywise.at[index, 'Est Imp'] = row['Est Imp'] / row['Total_Days']
    df_plan_daywise.at[index, 'Est Clicks'] = row['Est Clicks'] / row['Total_Days']
    df_plan_daywise.at[index, 'Total Net Cost'] = row['Total Net Cost'] / row['Total_Days']
    df_plan_daywise.at[index, 'Est Video Views'] = row['Est Video Views'] / row['Total_Days']

# Creating calculated columns(Website Visits)
try:
    for index, row in df_plan_daywise.iterrows():
        df_plan_daywise.at[index, 'Website Visits'] = row['Est Clicks'] * row['Click to Visits %']
except:
    print('Click to Visits % column not found')

    
# Plan to csv
df_plan_daywise.to_csv(f'{daywise_plans_path}{campaign_name}_plan_daywise.csv', index=False)
df_plan.to_csv(f'{overall_plans_path}{campaign_name}_plan_overall.csv', index=False)
print('Plan read successfully')