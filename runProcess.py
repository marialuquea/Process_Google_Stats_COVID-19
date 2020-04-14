# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:40:38 2020

@author: Maria

This file splits the PDFs from the folder gdata2020-4-10 and creates a new folder 'output' 
with all the 2-paged PDF of each country.

"""

import os
import glob
import csv
from PyPDF2 import PdfFileReader, PdfFileWriter
from country import CountryData, Sector

# split pages1 and 2 from every PDF
def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    for page in range(2):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = 'output/{}_{}.pdf'.format(fname, page+1)
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename))

# Merge pages 1 and 2 for every country
def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()
    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

# Get important values for each part (retail, grocery...)
def getValues(short):
    # Name
    sector = Sector(short[0][0])
    
    percentages = []
    dates = []
    months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ',
              'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
    for x in short:
        for i in x:
            if '%' in i:
                percentages.append(i)
            if any(word in i for word in months):
                dates.append(i)
    try:
        # Dates
        sector.startDate = dates[0]
        sector.endDate = dates[2]
        
        # Percentages
        percent_set = set(percentages)
        if len(percent_set) == 5: # if percentage is not 40% or 80%
            percentage = [ x for x in percent_set if "40" not in x and '80' not in x][0]
        else: # if percentage is either 40 or 80
            if percentages.count('+80%') == 2: percentage = '+80%'
            if percentages.count('-80%') == 2: percentage = '-80%'
            if percentages.count('+40%') == 2: percentage = '+40%'
            if percentages.count('-40%') == 2: percentage = '-40%'
        sector.percent = percentage
            
    except: print('')
    finally: return sector
    
    
def checkEmptyDates(final):
    try:
        final2 = []
        for i in range(0, len(final), 7):
            country = []
            date1 = ''
            date2 = ''
            if len(final[i]) == 1: country.append(final[i])
            for j in range(1,7): country.append(final[i+j])
            for a in country:
                if len(a) == 5: 
                    date1 = a[3]
                    date2 = a[4]
            for a in country:
                if len(a) == 3:
                    a.append(date1)
                    a.append(date2)
                final2.append(a)
    finally: return final2


def readCSV(path):
    dataset = []
    with open(path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            dataset.append(row)
    return dataset


if __name__ == '__main__':
    
#    # split first 2 pages of each country from folder gdata2020-04-10
#    # Change name of folder if PDFs are in another folder
#    paths = glob.glob('gdata2020-04-10/*.pdf')
#    for path in paths:
#        pdf_splitter(path)
#
#    # merge page 1 and 2 of each country and output them to folder PDFs
#    files = glob.glob('output/*.pdf') 
#    for page in range(0, len(files), 2):
#        paths = [files[page], files[page+1]]
#        name = "PDFs/" + files[page][18:35] +".pdf"
#        print(name, paths) 
#        merger(name, paths)
#    print("Success!")
#    
    
    # Read CSV files from folder CSVs
    paths = glob.glob('CSVs/*.csv')
    final = []
    for path in paths:
        
        dataset = readCSV(path)
        
        # Read only valuable information
        titles = ['Retail', 'Grocery', 'Parks', 'Transit', 'Work', 'Residential']
        
        countryName = dataset[1][0] + ' - ' + path[5:len(path)]
        country = CountryData(countryName)
        
        i = 0
        while i < len(dataset):
            if len(dataset[i]) != 0:
#                print(dataset[i])
                if any(word in dataset[i][0] for word in titles):
                    short = [[dataset[i][0]]]
                    for x in range(1, 12): # for the next 12 lines check if the section ends
                        try:
                            #when sector is complete
                            if any(word in dataset[i+x][0] for word in titles): 
                                sector = getValues(short)
                                country.add_sector(sector)
                                break
                            # keep adding info to sector until complete
                            else:
                                short.append(dataset[i+x])
                        except: 
                            if short[0][0] == 'Residential': 
                                sector = getValues(short)
                                if len(country.sectors) == 5:
                                    country.add_sector(sector)
                            print('...')
            i += 1
        
        print(country.name)
        for s in country.sectors:
            print(s.name.getSector())
            
        final.append([country.name])
        for sector in country.sectors:
            last = ['']
            for i in sector.name.getSector(): last.append(i)
            final.append(last)
        
        print("\n--END OF CSV FILE--\n")
        
        
    # Check for empty dates and correct
#    final = checkEmptyDates(final)

    # Save info to a file
    with open('final.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(final)
