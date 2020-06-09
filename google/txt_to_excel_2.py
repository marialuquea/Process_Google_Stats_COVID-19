# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 23:22:37 2020

@author: Maria
"""


import csv
import glob
import os

path = input('folder name: ')

#rename all files in folder
files = glob.glob(path + '/*.txt')
if 'InTextResults_001.txt' in files:
    print('Name of files already changed')
else:
    for file in files:
        name = file[-6:]
        try:
            name = name[:-4]
            int(name)
        except: name = name[1]
        os.rename(file, os.path.join(path, 'InTextResults_' + "%03d"%int(name) + '.txt'))

def read_file(path):
    dataset = []
    with open(path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader: dataset.append(row)
    return dataset

results = []
titles = []
files = glob.glob(path + '/*.txt')
count = 0
for p in files:
    count += 1
    print(p)
    dataset = read_file(p) # change file to path

    data = []
    for row in dataset:
        line = str(row).split(':') 
        for a in line:
            if a[:1] == "[": a = a[2:]
            if a[-1] == "]": a = a[:-4]
            if a != '': data.append(a)
            
    titles = []
    numbers = ["Results "+ str(count)]     
    for i in range(0, len(data), 2):
        titles.append(data[i])
        numbers.append(data[i+1])
        
    results.append(numbers)
   
titles.insert(0, "")
     
with open('9-6-20-inTextResults.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(titles)
    writer.writerows(results)
   
        
    
   