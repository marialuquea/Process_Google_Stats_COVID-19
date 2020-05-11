# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:58:14 2020

@author: Maria
"""

from urllib.request import urlopen
import json
from countryConvert import iso2_to_3
import pandas as pd
import csv
from datetime import date

url_start = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/'

date1 = input('Enter start date in the format YYYY-MM-DD:')
date2 = input('Enter end date in the format YYYY-MM-DD:')

# date1 = '2020-02-02'
# date2 = '2020-02-03'

url_final = url_start + date1 + '/' + date2

def save_file(filename, data, extension):
    if extension == 'json':
        with open(filename +'.json', 'w') as outfile:
            json.dump(data, outfile)
    if extension == 'csv':
        with open(filename + '.csv', 'w') as outfile:
            for key in data.keys():
                outfile.write("%s,%s\n"%(key,data[key]))

def check_exists(data, date1, country):
    try:
        hello = data['data'][date1][iso2_to_3(country)]['stringency_actual']
        return True
    except: return False

def count_days(date1, date2):
    f_date = date(int(date1[:4]), int(date1[5:7]), int(date1[8:]))
    l_date = date(int(date2[:4]), int(date2[5:7]), int(date2[8:]))
    delta = l_date - f_date
    print(delta.days)

def load_data():
    try:
        json_url = urlopen(url_final)
        data = json.loads(json_url.read())
        # save_file('oxford_values', data, 'json')
        xls = pd.ExcelFile('emissions_reduction_master_sheet.xlsx')
        df1 = pd.read_excel(xls, 'modal_trans_countries_covered')
        countries_covered = df1.iloc[1:130, 0]
        return countries_covered, data
    except Exception as e: print(e)
    return None


countries_covered, data = load_data()  
stringency_country = {}
for country in countries_covered:
    if check_exists(data, date1, country) == True:
        stringency_country[country] = data['data'][date1][iso2_to_3(country)]['stringency_actual']
        print(country, data['data'][date1][iso2_to_3(country)]['stringency_actual'])
    else: 
        stringency_country[country] = 'nan'
    
save_file('stringency_country', stringency_country, 'csv')



