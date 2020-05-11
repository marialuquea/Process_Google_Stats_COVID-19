# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:58:14 2020

@author: Maria
"""

from urllib.request import urlopen
import json
from countryConvert import convert_country_alpha3_to_country_alpha2

url_start = 'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/'

# date1 = input('Enter start date in the format YYYY-MM-DD:')
# date2 = input('Enter end date in the format YYYY-MM-DD:')

date1 = '2020-02-02'
date2 = '2020-02-03'

url_final = url_start + date1 + '/' + date2

def save_file(filename, data, extension):
    fileN = filename + '.' + extension
    with open(fileN, 'w') as outfile:
        json.dump(data, outfile)



try:
    json_url = urlopen(url_final)
    data = json.loads(json_url.read())
    # print(data)
    save_file('oxford_values', data, 'json')
    
    print(data['data']['2020-02-02']['AFG']['date_value'])
    print()
    print(data['data']['2020-02-02']['AFG'])
    print([convert_country_alpha3_to_country_alpha2('AFG')])
    print(data['data']['2020-02-02'][convert_country_alpha3_to_country_alpha2('AFG')])
    
except Exception as e: print(e)

