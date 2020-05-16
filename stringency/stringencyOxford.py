# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:22:33 2020

@author: Maria
"""

import pandas as pd
from countryConvert import iso2_to_3, country_to_iso2

#----------------------Read CSV from URL-----------------------------
data = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')

#----------------------Read Excel file-------------------------------
xls = pd.ExcelFile('emissions_reduction_master_sheet.xlsx')

regions = pd.read_excel(xls, 'Regional_shares')
countries = (regions.iloc[6:218, 0]).reset_index(drop=True)


# Organise countries by regions 
regions_list = {}
for index, row in regions.iterrows(): 
    if row['Region'] in regions_list:
        # print('if')
        before = regions_list[row['Region']]
        before.append(row['Country Name'])
        regions_list[row['Region']] = before
    else:
        # for non used countries
        if 'nan' in str(row['Region']): regions_list[0] = [row['Country Name']]
        # start region list
        # print(row['Region'], row['Country Name'], country_to_iso2(row['Country Name']))
        else: regions_list[row['Region']] = [row['Country Name']]
del regions_list[0]



# Set each name to also have iso3 name before
countries_list = []
for region, country_list in regions_list.items():
    if len(country_list) == 1:
        regions_list[region] = [iso2_to_3(country_to_iso2(country_list[0]))  + ',' + country_list[0]]
        print(region, regions_list[region])
        countries_list.append(regions_list[region][0])
    else:
        new_list = []
        for country in country_list:
            if country == 'Zanzibar': 
                new_list.append( country_to_iso2(country)  + ',' + country)
                countries_list.append(country_to_iso2(country)  + ',' + country)
            else:
                new_list.append( iso2_to_3(country_to_iso2(country)) + ',' + country)
                countries_list.append(iso2_to_3(country_to_iso2(country)) + ',' + country)
        print(region, new_list)
        regions_list[region] = new_list


# Remove ZZZZs (Kosovo)
count, idx = 0, 0
for c in countries_list:
    if len(c.split(',')[0]) != 3: idx=count
    count += 1
del countries_list[idx]
countries_list.sort()


# del row, index, regions, before, c, countries, xls, country_list, new_list, country, region, idx, count
        
     
   
#--------------------- Read country's stringencies
stringency_countries = {}
for country in countries_list:
    stringency_countries[country] = 'nan'

    
# date = input('Enter start date in the format YYYYMMDD:')
date = '20200507' 

for index, row in data.iterrows():   
    if row['Date'] == int(date):    
        # print(key in stringency_countries if row['CountryCode'] in key)
        countryName = [key for key,val in stringency_countries.items() if row['CountryCode'] in key[:3]]
        if len(countryName) != 0 and countryName[0] in stringency_countries:
            stringency = [row['LegacyStringencyIndexForDisplay'] for key,val in stringency_countries.items() if row['CountryCode'] in key]
            stringency_countries[countryName[0]] = stringency[0]


{k: v for k, v in sorted(stringency_countries.items(), key=lambda item: item[0])}
for key, value in stringency_countries.items():
    if str(value) == 'nan': stringency_countries[key] = 'nan'

# del countryName, index, row, stringency, key, value, country
    
    
 
    

#------------------- Put stringencies in regions
for region, country_list in regions_list.items():
    # print(region, country_list)
    if len(country_list) == 1 and 'list' in str(type(country_list)):
        regions_list[region] = {country_list[0] : [val for key, val in stringency_countries.items() if country_list[0] in key][0]}
    else: # more than one country per region 
        new_dict = {}
        for country in country_list:
            res = dict(filter(lambda item: country in item[0], stringency_countries.items()))
            if len(res) != 0 and country in stringency_countries:
                # print ('res:',res, '\t', country, res[country])
                new_dict[country] = res[country]
        regions_list[region] = new_dict
        

#---------------------Calculate average per region
for region, country_list in regions_list.items():
    if len(country_list.keys()) > 1:
        values = [i for i in country_list.values() if i != 'nan']
        avg = sum(values) / float(len(values))
        regions_list[region]['average'] = avg

#----------------------Save results to csv---------------------------
with open('stringency_20200507_1.csv', 'w') as f:
    f.write('%s,%s,%s,%s\n'%('Region', 'Stringency', 'Date:',date))
    for region, country_list in regions_list.items():
        if len(country_list.keys()) == 1:
            f.write("%s,%s\n"%(region, list(country_list.values())[0]))
        else:
            f.write("%s,%s,,"%(region, 
                              country_list['average']))
            for key, value in country_list.items():
                f.write("%s,%s,"%(key, value))
            f.write("\n")
        
        
 

# del before, c, count, countries, country, countryCode, country_iso3, country_list, country_list_before, country_name, ele, f, i, index, new_dict, region, res, row, stringency, sumation, values, without_nan, xls

    