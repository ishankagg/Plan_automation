import pandas as pd
import datetime
import numpy
# from plyer import notification


ravish_report_path = 'Ravish_Format\Ravish Report Digital Final.xlsx'
merged_plan_report_path = 'merged_plan_report.csv'
t_date = '20-07-2024'
t_date = pd.to_datetime(t_date, format='%d-%m-%Y')

#Reading the report
ravish_report = pd.read_excel(ravish_report_path, sheet_name='Data')

#Reading the merged plan report
merged_plan_report = pd.read_csv(merged_plan_report_path)

# Replace the values in the 'Geo' column and assign it back to the DataFrame
merged_plan_report['Geo'] = merged_plan_report['Geo'].replace({
    'Delhi NCR Booster': 'Delhi NCR',
    'ROC1': 'RO C1',
})


# merged_plan_report.columns

# ravish_report.columns
merged_plan_report['Day'] = ''

# Ensure 'Date' column is in datetime format
merged_plan_report['Date'] = pd.to_datetime(merged_plan_report['Date'], format = '%Y-%m-%d')
merged_plan_report['Date']

# for i in range(len(merged_plan_report['Date'])):
#     merged_plan_report['Day'][i] = 'T-' + str((pd.to_datetime(t_date) - pd.to_datetime(merged_plan_report['Date'][i])).days)
#     print(merged_plan_report['Day'][i], merged_plan_report['Date'][i])

# Calculate the difference in days and format the 'Day' column
merged_plan_report['Day'] = 'T-' + (pd.to_datetime(t_date) - merged_plan_report['Date']).dt.days.astype(str)

# Format the 'Date' column to DD-MM-YYYY
merged_plan_report['Date'] = merged_plan_report['Date'].dt.strftime('%d-%m-%Y')

merged_plan_report['Day']

ravish_report_format = merged_plan_report.loc[:,['Date', 'Day', 'Geo', 'Planned Impressions','Delivered Impressions', 'Planned Clicks', 'Delivered Clicks', 'Planned Video Views', '100% Views','Planned Spends','Delievered Spends']]

ravish_report_format = ravish_report_format.sort_values(by=['Date', 'Geo'])

ravish_report_format = ravish_report_format.groupby(['Date', 'Day', 'Geo']).agg({
    'Planned Impressions': 'sum',
    'Delivered Impressions': 'sum',
    'Planned Clicks': 'sum',
    'Delivered Clicks': 'sum',
    'Planned Video Views': 'sum',
    '100% Views': 'sum',
    'Planned Spends': 'sum',
    'Delievered Spends': 'sum'
}).reset_index()

ravish_report_format

ravish_report_format = ravish_report_format.rename(columns={
    'Day':'day',
    'Geo':'geocity',
    'Planned Impressions': 'cyplannedimpressions24',
    'Delivered Impressions': 'cydeliveredimpressions24',
    'Planned Clicks': 'cyplannedclicks24',
    'Delivered Clicks': 'cydeliveredclicks24',
    'Planned Video Views': 'cyplannedviews24',
    '100% Views': 'cydeliveredviews24',
    'Planned Spends': 'cyplannedspends24',
    'Delievered Spends': 'cydeliveredspends24'

})

ravish_report_format

ravish_report_format.to_csv('ravish_report_format.csv', index=False)

ravish_report_format['Date'] = pd.to_datetime(ravish_report_format['Date'], dayfirst=True)


ravish_report_final = pd.merge(ravish_report, ravish_report_format, on = ['Date','day','geocity'], how='left', suffixes=('_x', '_y'))


# Replace common columns in left_df with those from right_df
common_columns = set(ravish_report.columns).intersection(set(ravish_report_format.columns)) - {'Date', 'day', 'geocity'}
for col in common_columns:
    ravish_report_final[col] = ravish_report_final[col + '_y']
    ravish_report_final.drop(columns=[col + '_x', col + '_y'], inplace=True)

# Creating calculated columns
ravish_report_final.columns

ravish_report_final['deliveredimpressionpercent'] = (ravish_report_final['cydeliveredimpressions24'] / ravish_report_final['cyplannedimpressions24'])
ravish_report_final['lydeliveredimpressionpercent'] = (ravish_report_final['lydeliveredimpressions'] / ravish_report_final['lyplannedimpressions'])
ravish_report_final['deliveredimpressionsvsly'] = (ravish_report_final['deliveredimpressionpercent'] / ravish_report_final['deliveredimpressionpercent'])
ravish_report_final['deliveredviewspercent'] = (ravish_report_final['cydeliveredviews24'] / ravish_report_final['cyplannedviews24'])
ravish_report_final['lydeliveredviewspercent'] = (ravish_report_final['lydeliveredviews'] / ravish_report_final['lyplannedviews'])
ravish_report_final['deliveredviewsvsly'] = (ravish_report_final['deliveredviewspercent'] / ravish_report_final['deliveredviewspercent'])
ravish_report_final['plannedctr'] = (ravish_report_final['cyplannedclicks24'] / ravish_report_final['cyplannedimpressions24'])
ravish_report_final['lyplannedctr'] = (ravish_report_final['lyplannedclicks'] / ravish_report_final['lyplannedimpressions'])
ravish_report_final['deliveredctr'] = (ravish_report_final['cydeliveredclicks24'] / ravish_report_final['cydeliveredimpressions24'])
ravish_report_final['lydeliveredctr'] = (ravish_report_final['lydeliveredclicks'] / ravish_report_final['lydeliveredimpressions'])
ravish_report_final['deliveredctrpercent'] = (ravish_report_final['deliveredctr'] / ravish_report_final['lydeliveredctr'])
ravish_report_final['lydeliveredctrpercent'] = (ravish_report_final['lydeliveredctr'] / ravish_report_final['lydeliveredctr'])
ravish_report_final['deliveredctrvsly'] = (ravish_report_final['deliveredctrpercent'] / ravish_report_final['lydeliveredctrpercent'])
ravish_report_final['plannedvtr'] = (ravish_report_final['cyplannedviews24'] / ravish_report_final['cyplannedimpressions24'])
ravish_report_final['lyplannedvtr'] = (ravish_report_final['lyplannedviews'] / ravish_report_final['lyplannedimpressions'])
ravish_report_final['deliveredvtr'] = (ravish_report_final['cydeliveredviews24'] / ravish_report_final['cydeliveredimpressions24'])
ravish_report_final['lydeliveredvtr'] = (ravish_report_final['lydeliveredviews'] / ravish_report_final['lydeliveredimpressions'])
ravish_report_final['deliveredvtrpercent'] = (ravish_report_final['deliveredvtr'] / ravish_report_final['lydeliveredvtr'])
ravish_report_final['lydeliveredvtrpercent'] = (ravish_report_final['lydeliveredvtr'] / ravish_report_final['lydeliveredvtr'])
ravish_report_final['deliveredvtrvsly'] = (ravish_report_final['deliveredvtrpercent'] / ravish_report_final['lydeliveredvtrpercent'])
ravish_report_final['deliveredclickspercent'] = (ravish_report_final['cydeliveredclicks24'] / ravish_report_final['cyplannedclicks24'])
ravish_report_final['lydeliveredclickspercent'] = (ravish_report_final['lydeliveredclicks'] / ravish_report_final['lyplannedclicks'])
ravish_report_final['deliveredclicksvsly'] = (ravish_report_final['deliveredclickspercent'] / ravish_report_final['lydeliveredclickspercent'])
ravish_report_final['deliveredspendspercent'] = (ravish_report_final['cydeliveredspends24'] / ravish_report_final['cyplannedspends24'])
ravish_report_final['lydeliveredspendspercent'] = (ravish_report_final['lydeliveredspends'] / ravish_report_final['lyplannedspends'])
ravish_report_final['deliveredspendsvsly'] = (ravish_report_final['deliveredspendspercent'] / ravish_report_final['lydeliveredspendspercent'])

# Reorder columns
ravish_report_final = ravish_report_final.loc[:,["Date", "day", "geocity", "cyplannedimpressions24", "lyplannedimpressions", "cydeliveredimpressions24", "lydeliveredimpressions", "deliveredimpressionpercent", "lydeliveredimpressionpercent", "deliveredimpressionsvsly", "cyplannedviews24", "lyplannedviews", "cydeliveredviews24", "lydeliveredviews", "deliveredviewspercent", "lydeliveredviewspercent", "deliveredviewsvsly", "plannedctr", "lyplannedctr", "deliveredctr", "lydeliveredctr", "deliveredctrpercent", "lydeliveredctrpercent", "deliveredctrvsly", "plannedvtr", "lyplannedvtr", "deliveredvtr", "lydeliveredvtr", "deliveredvtrpercent", "lydeliveredvtrpercent", "deliveredvtrvsly", "cyplannedclicks24", "lyplannedclicks", "cydeliveredclicks24", "lydeliveredclicks", "deliveredclickspercent", "lydeliveredclickspercent", "deliveredclicksvsly", "cyplannedspends24", "lyplannedspends", "cydeliveredspends24", "lydeliveredspends", "deliveredspendspercent", "lydeliveredspendspercent", "deliveredspendsvsly"]]

ravish_report_final.to_csv('ravish_report.csv', index=False)

print('Ravish Report Generated')

