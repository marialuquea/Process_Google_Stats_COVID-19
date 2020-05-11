# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:22:33 2020

@author: Maria
"""

import pandas as pd
from countryConvert import iso2_to_3, iso3_to_2, iso2_to_country_name
from collections import OrderedDict


#----------------------Read CSV from URL-----------------------------
data = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')

#----------------------Read Excel file-------------------------------
xls = pd.ExcelFile('emissions_reduction_master_sheet.xlsx')

df1 = pd.read_excel(xls, 'modal_trans_countries_covered')
countries_covered = df1.iloc[1:130, 0]

regions = pd.read_excel(xls, 'Regional_shares')



regions_list = {}
for index, row in regions.iterrows(): 
    if row['Region'] in regions_list:
        before = regions_list[row['Region']]
        before.append(row['Country Name'])
        regions_list[row['Region']] = before
    else:
        regions_list[row['Region']] = [row['Country Name']]
del regions_list[0]



# Read country's stringencies
stringency_countries = {}
for country in countries_covered:
    stringency_countries[iso2_to_3(country)] = 'nan'
# date = input('Enter start date in the format YYYYMMDD:')
date = '20200505' 

for index, row in data.iterrows():                      # for every row of the csv published
    if row['Date'] == int(date):                        # if the date is the selected one
        if row['CountryCode'] in stringency_countries:  # if the country is in countries covered
            stringency_countries[row['CountryCode']] = row['LegacyStringencyIndexForDisplay']

od=OrderedDict(sorted(stringency_countries.items()))


#------------------ Make List have ISO2 names
keys = list(od.keys())
values = list(od.values())
for i in range(len(od)):
    country_iso3 = keys[i]
    stringency = values[i]
    iso2_name = iso3_to_2(country_iso3)
    country_name = iso2_to_country_name(iso2_name)
    od[country_name] = od.pop(country_iso3)

#------------------- Process regions and stringencies
for region, country_list in regions_list.items():
    # print(region, country_list)
    if len(country_list) == 1 and 'list' in str(type(country_list)):
        if country_list[0] in od:
            regions_list[region] = {country_list[0] : od[country_list[0]]}
        else:
            regions_list[region] = {country_list[0] : 'nan'}
    else: # more than one country per region 
        country_list_before = country_list.copy()
        
        new_dict = {}
        for country in country_list_before:
            if country in od: new_dict[country] = od[country]
            else: new_dict[country] = 'nan'
        regions_list[region] = new_dict
        

#---------------------Calculate average per region
for region, country_list in regions_list.items():
    if len(country_list.keys()) > 1:
        print(region)

#----------------------Save results to csv---------------------------
with open('stringencyOxford.csv', 'w') as f:
    for key in stringency_countries.keys():
        f.write("%s,%s\n"%(key,stringency_countries[key]))


    