#--------------------------------------
#
#   This file cleans Homeownership Rate, Rental Vacancy Rate, and Homeowner Vacancy Rate data by MSA from the Census
#   Housing Vacancies and Homeownership (CPS/HVS) statistics: https://www.census.gov/housing/hvs/data/rates.html
#
#   The code produces three .csv files with data for:
#       - Homeownership (rate)
#       - Rental Vacancy (rate)
#       - Homeowner Vacancy (rate)
#
#   Data are available quarterly from 2005:Q1-2018:Q1 (can be updated with data from the website above).
#
#--------------------------------------

import numpy as np
import pandas as pd
import requests

#------------------------------------------------------
# Set-up
#------------------------------------------------------

census_url = 'https://www.census.gov/housing/hvs/data/rates/'

excelnames = ['tab4a_msa_05_2014_rvr', 'tab4_msa_15_18_rvr',
              'tab6a_msa_05_2014_hmr', 'tab6_msa_15_18_hmr',
              'tab5a_msa_05_2014_hvr', 'tab5_msa_15_18_hvr']

quarters = ['Q1', 'Q2', 'Q3', 'Q4']

# MSA names changed between the two data sets.
# This option allows you to convert the old MSA names to new MSA names, or vice versa.
# use_new = -1 (Convert new to old names),
#            0 (Do not convert names),
#            1 (Convert old to new names)
use_new = 1

#------------------------------------------------------
# Download and save XLSX files from Census website into current directory
#------------------------------------------------------

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
#------------------------------------------------------

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
# New-to-old (or, Old-to-new) names for conversion
#------------------------------------------------------

# Key: New Name, Value: Old Name
new_to_old = {'Atlanta-Sandy Springs-Roswell, GA': 'Atlanta-Sandy Springs-Marietta, GA',
              'Baltimore-Columbia-Towson, MD': 'Baltimore-Towson, MD',
              'Boston-Cambridge-Newton, MA-NH': 'Boston-Cambridge-Quincy, MA-NH',
              'Buffalo-Cheektowaga-Niagara Falls, NY': 'Buffalo-Cheektowaga-Tonawanda, NY',
              'Charlotte-Concord-Gastonia, NC-SC': 'Charlotte-Gastonia-Concord, NC-SC',
              'Chicago-Naperville-Elgin, IL-IN-WI': 'Chicago-Naperville-Joliet, IL',
              'Cincinnati, OH-KY-IN': 'Cincinnati-Middletown, OH-KY-IN',
              'Cleveland-Elyria, OH': 'Cleveland-Elyria-Mentor, OH',
              'Denver-Aurora-Lakewood, CO': 'Denver-Aurora, CO',
              'Detroit-Warren-Dearborn, MI': 'Detroit-Warren-Livonia, MI',
              'Houston-The Woodlands-Sugar Land, TX': 'Houston-Baytown-Sugar Land, TX',
              'Indianapolis-Carmel-Anderson, IN': 'Indianapolis, IN',
              'Las Vegas-Henderson-Paradise, NV': 'Las Vegas-Paradise, NV',
              'Los Angeles-Long Beach-Anaheim, CA': 'Los Angeles-Long Beach-Santa Ana, CA',
              'Louisville/Jefferson County, KY-IN': 'Louisville, KY-IN',
              'Miami-Fort Lauderdale-West Palm Beach, FL': 'Miami-Fort Lauderdale-Miami Beach, FL',
              'Nashville-Davidson-Murfreesboro-Franklin, TN': 'Nashville-Davidson-Murfreesboro, TN',
              'New Orleans-Metairie, LA': 'New Orleans-Metairie-Kenner, LA',
              'New York-Newark-Jersey City, NY-NJ-PA': 'New York-Northern New Jersey--Long Island, NY',
              'Orlando-Kissimmee-Sanford, FL': 'Orlando, FL',
              'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD': 'Philadelphia-Camden-Wilmington, PA',
              'Portland-Vancouver-Hillsboro, OR-WA': 'Portland-Vancouver-Beaverton, OR-WA',
              'Providence-Warwick, RI-MA': 'Providence-New Bedford-Fall River, RI-MA',
              'Raleigh, NC': 'Raleigh-Cary, NC',
              'Sacramento-Roseville-Arden-Arcade, CA': 'Sacramento-Arden-Arcade-Roseville, CA',
              'San Antonio-New Braunfels, TX': 'San Antonio, TX',
              'San Diego-Carlsbad, CA': 'San Diego-Carlsbad-San Marco, CA',
              'San Francisco-Oakland-Hayward, CA': 'San Francisco-Oakland-Fremont, CA',
              'Urban Honolulu, HI': 'Honolulu, HI',
              'Virginia Beach-Norfolk-Newport News, VA-NC': 'Virginia Beach-Norfolk-Newport News, VA'}

# Key: Old Name, Value: New Name
old_to_new = {v: k for k, v in new_to_old.items()}

#------------------------------------------------------
# Import, clean, format, and save the Homeownership Rate data
#------------------------------------------------------

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

# Modify MSA names
if (use_new==-1):
    # Rename all new names in df_rvr_15_18 with the old names
    for new_name in list(new_to_old.keys()):
        old_name = old_to_new[new_name]
        df_hmr_15_18.loc[df_hmr_15_18['MSA_Name']==new_name, 'MSA_Name'] = old_name
elif (use_new==1):
    # Rename all old names in df_hmr_05_14 with the new names
    for old_name in list(old_to_new.keys()):
        new_name = old_to_new[old_name]
        df_hmr_05_14.loc[df_hmr_05_14['MSA_Name']==old_name, 'MSA_Name'] = new_name


# Merge the two data tables
df_hmr = df_hmr_05_14.append(df_hmr_15_18)
df_hmr = df_hmr.sort_values(['MSA_Name', 'Year', 'Quarter'])

# Save to CSV
df_hmr.to_csv('Census_HomeownershipRate.csv', index=False)

#------------------------------------------------------
# Import, clean, format, and save the Rental Vacancy Rate data
#------------------------------------------------------

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

# Modify MSA names
if (use_new==-1):
    # Rename all new names in df_rvr_15_18 with the old names
    for new_name in list(new_to_old.keys()):
        old_name = old_to_new[new_name]
        df_rvr_15_18.loc[df_rvr_15_18['MSA_Name']==new_name, 'MSA_Name'] = old_name
elif (use_new==1):
    # Rename all old names in df_rvr_05_14 with the new names
    for old_name in list(old_to_new.keys()):
        new_name = old_to_new[old_name]
        df_rvr_05_14.loc[df_rvr_05_14['MSA_Name']==old_name, 'MSA_Name'] = new_name



# Merge the two data tables
df_rvr = df_rvr_05_14.append(df_rvr_15_18)
df_rvr = df_rvr.sort_values(['MSA_Name', 'Year', 'Quarter'])

# Save to CSV
df_rvr.to_csv('Census_RentalVacancyRate.csv', index=False)

#------------------------------------------------------
# Import, clean, format, and save the Homeowner Vacancy Rate data
#------------------------------------------------------

# Get first HVR table: 2005-2014
csvname = 'tab5a_msa_05_2014_hvr.csv'
value_name = 'HomeownerVacancyRate'
yearlist = list(range(2005, 2015))
yearlist = list(reversed(yearlist))

df_hvr_05_14 = get_clean_data(csvname)
df_hvr_05_14 = get_formatted_table(df_hvr_05_14, yearlist, value_name)


# Get second HVR table: 2015-2018
csvname = 'tab5_msa_15_18_hvr.csv'
value_name = 'HomeownerVacancyRate'
yearlist = list(range(2015, 2019))
yearlist = list(reversed(yearlist))

df_hvr_15_18 = get_clean_data(csvname)
df_hvr_15_18 = get_formatted_table(df_hvr_15_18, yearlist, value_name)

# Modify MSA names
if (use_new==-1):
    # Rename all new names in df_hvr_15_18 with the old names
    for new_name in list(new_to_old.keys()):
        old_name = old_to_new[new_name]
        df_hvr_15_18.loc[df_hvr_15_18['MSA_Name']==new_name, 'MSA_Name'] = old_name
elif (use_new==1):
    # Rename all old names in df_hvr_05_14 with the new names
    for old_name in list(old_to_new.keys()):
        new_name = old_to_new[old_name]
        df_hvr_05_14.loc[df_hvr_05_14['MSA_Name']==old_name, 'MSA_Name'] = new_name


# Merge the two data tables
df_hvr = df_hvr_05_14.append(df_hvr_15_18)
df_hvr = df_hvr.sort_values(['MSA_Name', 'Year', 'Quarter'])

# Save to CSV
df_rvr.to_csv('Census_HomeownerVacancyRate.csv', index=False)
