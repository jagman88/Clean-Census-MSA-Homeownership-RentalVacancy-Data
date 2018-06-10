#--------------------------------------
#
#   This file cleans Homeownership Rate and Rental Vacancy Rate data by MSA from the Census
#   Housing Vacancies and Homeownership (CPS/HVS) statistics: https://www.census.gov/housing/hvs/data/rates.html
#
#   The code produces two .csv files with data for:
#       - Homeownership (rate)
#       - Rental Vacancy (rate)
#
#   Data are available quarterly from 2005:Q1-2018:Q1 (can be updated with data from the website above).
#
#--------------------------------------

import pandas as pd
import requests

#------------------------------------------------------
# Set-up

census_url = 'https://www.census.gov/housing/hvs/data/rates/'

excelnames = ['tab4a_msa_05_2014_rvr', 'tab4_msa_15_18_rvr', 'tab6a_msa_05_2014_hmr', 'tab6_msa_15_18_hmr']

quarters = ['Q1', 'Q2', 'Q3', 'Q4']

#------------------------------------------------------
# Download and save XLSX files from Census website into current directory
for xx in excelnames:
    dls = census_url+xx+'.xlsx'
    resp = requests.get(dls)

    output = open(xx+'.xlsx', 'wb')
    output.write(resp.content)
    output.close()

# Convert XLSX files to CSV, save to current directory
for xx in excelnames:
    data_xls = pd.read_excel(xx+'.xlsx', index_col=None)
    data_xls.to_csv(xx+'.csv', index=False)

#------------------------------------------------------
# Functions to clean and format the data tables

def get_clean_data(csvname):

    # Import data
    df_tmp = pd.read_csv(csvname,
                         skiprows=[0,1,2, 4, 5, 6, 7],
                         usecols=[1,2,4,6,8],
                         engine='python',
                         skipfooter=3)

    # Rename columns
    df_tmp.columns = ['MSA_Name', quarters[0], quarters[1], quarters[2], quarters[3]]

    # Remove leading and trailing white space
    df_tmp['MSA_Name'] = df_tmp['MSA_Name'].str.strip()
    # Remove numbers
    df_tmp['MSA_Name'] = df_tmp['MSA_Name'].str.replace('\d+', '')

    # Only keep letters, internal spaces, commans, and dashes
    df_tmp['MSA_Name'] = df_tmp['MSA_Name'].str.replace('([^\s\w+,\w+-]|_)+', '')

    # Only keep MSA variables
    df_tmp = df_tmp.loc[(df_tmp['MSA_Name']!='Metropolitan Statistical Area')&
                        (df_tmp['MSA_Name'].notnull())]
    # Remove remaining trailing whitespace
    df_tmp['MSA_Name'] = df_tmp['MSA_Name'].str.strip()

    return df_tmp


def get_formatted_table(df_tmp, yearlist, value_name):

    # Get Year for each row
    msanames = np.unique(df_tmp['MSA_Name'].astype(str))
    for mm in msanames:
        df_tmp.loc[df_tmp['MSA_Name']==mm, 'Year'] = yearlist
    df_tmp['Year'] = df_tmp['Year'].astype(int)

    # Get long format
    df_tmp = df_tmp.melt(id_vars=['MSA_Name', 'Year'], var_name='Quarter', value_name=value_name)

    # Order by MSA, Year, Quarter
    df_tmp = df_tmp.sort_values(['MSA_Name', 'Year', 'Quarter'])

    return df_tmp

#------------------------------------------------------
# Import, clean, format, and save the Homeownership Rate data

# Get first Homeownership rate table: 2005-2014
csvname = 'tab6a_msa_05_2014_hmr.csv'
value_name = 'HomeOwnershipRate'
yearlist = list(range(2005, 2015))
yearlist = list(reversed(yearlist))

df_hmr_05_14 = get_clean_data(csvname)
df_hmr_05_14 = get_formatted_table(df_hmr_05_14, yearlist, value_name)


# Get second Homeownership rate table: 2015-2018
csvname = 'tab6_msa_15_18_hmr.csv'
value_name = 'HomeOwnershipRate'
yearlist = list(range(2015, 2019))
yearlist = list(reversed(yearlist))

df_hmr_15_18 = get_clean_data(csvname)
df_hmr_15_18 = get_formatted_table(df_hmr_15_18, yearlist, value_name)


# Merge the two data tables
df_hmr = df_hmr_05_14.append(df_hmr_15_18)
df_hmr = df_hmr.sort_values(['MSA_Name', 'Year', 'Quarter'])

# Save to CSV
df_hmr.to_csv('Census_HomeownershipRate.csv', index=False)

#------------------------------------------------------
# Import, clean, format, and save the Rental Vacancy Rate data

# Get first RVR table: 2005-2014
csvname = 'tab4a_msa_05_2014_rvr.csv'
value_name = 'RentalVacancyRate'
yearlist = list(range(2005, 2015))
yearlist = list(reversed(yearlist))

df_rvr_05_14 = get_clean_data(csvname)
df_rvr_05_14 = get_formatted_table(df_rvr_05_14, yearlist, value_name)


# Get second RVR table: 2015-2018
csvname = 'tab4_msa_15_18_rvr.csv'
value_name = 'RentalVacancyRate'
yearlist = list(range(2015, 2019))
yearlist = list(reversed(yearlist))

df_rvr_15_18 = get_clean_data(csvname)
df_rvr_15_18 = get_formatted_table(df_rvr_15_18, yearlist, value_name)


# Merge the two data tables
df_rvr = df_rvr_05_14.append(df_rvr_15_18)
df_rvr = df_rvr.sort_values(['MSA_Name', 'Year', 'Quarter'])

# Save to CSV
df_rvr.to_csv('Census_RentalVacancyRate.csv', index=False)
