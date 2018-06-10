# Clean Census MSA-level Homeownership and Vacancy Rate Data

This file cleans Homeownership Rate and Rental Vacancy Rate data by MSA from the Census Housing Vacancies and Homeownership (CPS/HVS) statistics. The raw text files are not easy to manipulate, and are in an unusable format for MSA-by-MSA time series analysis. This code cleans and formats, leaving the data in long-form for ease of use as panel data. Note that the code can be modified to clean Homeowner Vacancy rates, or to clean the state-level data. Both of these are also available at the Census website.

Comments and suggestions most welcome.  

# Getting Started

Census data are available quarterly from 2005:Q1-2018:Q1, and can be found at: <https://www.census.gov/housing/hvs/data/rates.html>.
The code downloads raw data from the Census website, and converts the files to .csv format for ease of reading and manipulation.

# Code output

The code produces two .csv files with the following columns.

- MSA_Name
- Year
- Quarter
- HomeOwnershipRate/RentalVacancyRate

The resulting .csv files are approximately 166kb in size.

# Prerequisites

The script requires 'Python' along with the 'pandas' and 'requests' libraries.

# Running the code

The code can be run directly from the command line via:
'''
python Census_MSA_Homeownership_RentalVacancies.py
'''

# Author

- James Graham (NYU, 2018)

# License

This project is licensed under the MIT License.
