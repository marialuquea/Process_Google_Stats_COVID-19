# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:19:34 2020

@author: Maria
"""
import csv
import glob
import os


#rename all files in folder
path = '0706'
files = glob.glob(path + '/*.txt')
if 'scenario_001.txt' in files:
    print('Name of files already changed')
else:
    for file in files:
        name = file[-6:]
        try:
            name = name[:-4]
            int(name)
            # print('YAY', name)
        except:
            name = name[1]
            # print('except: ',name)
        os.rename(file, os.path.join(path, 'scenario_' + "%03d"%int(name) + '.txt'))


def read_file(path):
    dataset = []
    with open(path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader:
            dataset.append(row)
    return dataset


titles = []
regions = []
GHG_reduction = []
PM2_reduction = []
SO2_reduction = []
NOx_reduction = []
    
    
paths = glob.glob('0706/*.txt')
for path in paths:
    print(path)
    dataset = read_file(path)

    scenario = []
    for row in dataset:
        line = str(row).split('\\t') # split item in row by tabs
        line.pop(5) # remove the last element of list ('])
        line[0] = line[0][2:] # remove the first 2 letters of first element ([')
        scenario.append(line)

    titles = scenario.pop(0)
    titles[3] = 'SO2 reduction (%)'
    regions = []
    
    for a in scenario: 
        regions.append(a[0])
        GHG_reduction.append(a[1])
        PM2_reduction.append(a[2])
        SO2_reduction.append(a[3])
        NOx_reduction.append(a[4])
   
# final CSV files
GHG_final = [] # column 1
PM2_final = [] # column 2
SO2_final = [] # column 3
NOx_final = [] # column 4

def processColumn(column):
    # first row - title and scenarios
    scenarios = [titles[column]]
    for i in range(len(paths)): scenarios.append('Scenario ' + str(i+1))  
    if column == 1: GHG_final.append(scenarios)
    if column == 2: PM2_final.append(scenarios)
    if column == 3: SO2_final.append(scenarios)
    if column == 4: NOx_final.append(scenarios)
    
    for i in range(len(regions)):  # for i in range 38
        new_row = [regions[i]] # region name 
        for j in range(len(scenarios) - 1): # for every scenario
            # print(i+(38*(j)), GHG_reduction[i+(38*(j))])
            if column == 1: new_row.append(GHG_reduction[i+(38*(j))])
            # print('new_row\t',new_row)
            if column == 2: new_row.append(PM2_reduction[i+(38*(j))])
            if column == 3: new_row.append(SO2_reduction[i+(38*(j))])
            if column == 4: new_row.append(NOx_reduction[i+(38*(j))])
        if column == 1: GHG_final.append(new_row)
    # print('GHG_final\t',GHG_final)
        if column == 2: PM2_final.append(new_row)
        if column == 3: SO2_final.append(new_row)
        if column == 4: NOx_final.append(new_row)
    
    
def save_file(name, column):
    with open(name+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if column == 1: writer.writerows(GHG_final)
        if column == 2: writer.writerows(PM2_final)
        if column == 3: writer.writerows(SO2_final)
        if column == 4: writer.writerows(NOx_final)
        
processColumn(1)
save_file('GHG_regions_bytotal_scenarios', 1)
processColumn(2)
save_file('PM2_regions_bytotal_scenarios', 2)
processColumn(3)
save_file('SO2_regions_bytotal_scenarios', 3)
processColumn(4)
save_file('NOx_regions_bytotal_scenarios', 4)

# del row, line, a, path, dataset, scenario, i, j, writer, new_row, csvfile
    