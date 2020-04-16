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
from operator import itemgetter

# split pages1 and 2 from every PDF
def pdf_splitter(path, output):
    try:
        fname = os.path.splitext(os.path.basename(path))[0]
        pdf = PdfFileReader(path)
        for page in range(2):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = output+'/{}_{}.pdf'.format(fname, page+1)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            print('Created: {}'.format(output_filename))
    except Exception as e: print(e)

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
    
    dates = []
    months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ',
              'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
    for x in short:
        for i in x:
            if any(word in i for word in months):
                dates.append(i)
    try:
        # Dates - might be empty
        sector.startDate = dates[0]
        sector.endDate = dates[2]
        
    except: pass
    finally: return sector
    
    
def checkEmptyDates(final):
    try:
        for country in final:
            date1 = ''
            date2 = ''
            for sector in country.sectors:
                if sector.name.startDate != '': date1 = sector.name.startDate
                if sector.name.endDate != '': date2 = sector.name.endDate
            for sector in country.sectors:
                if sector.name.startDate == '': sector.name.startDate = date1
                if sector.name.endDate == '': sector.name.endDate = date2
    except Exception as e:
        print('checkEmptyDates\t\t',e)
    finally: 
        return final


def getPercentage(percentages):
    # Clean list from unwanted info
    percentages = [x for x in percentages if '* Not' not in x]
    
    final = []
    percentage = ''
    for i in range(0, len(percentages), 5):
        short = []
        for j in range(5):
            short.append(percentages[i+j])
        percent_set = set(short)
        if len(percent_set) == 5: # if percentage is not 40% or 80%
            percentage = [ x for x in percent_set if "40" not in x and '80' not in x][0]
        else: # if percentage is either 40 or 80
            if percentages.count('+80%') == 7: percentage = '+80%'
            if percentages.count('-80%') == 7: percentage = '-80%'
            if percentages.count('+40%') == 7: percentage = '+40%'
            if percentages.count('-40%') == 7: percentage = '-40%'
        final.append(percentage)
    return final
    

def readCSV(path):
    dataset = []
    with open(path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            dataset.append(row)
    return dataset

def checkDuplicates(country):
    already_there = []
    duplicates = []
    for s in country.sectors: already_there.append(s.name.getSector()[0])
    for s in already_there:
        if already_there.count(s) > 1: duplicates.append(s)
    for s in country.sectors:
        if any(word in s.name.getSector()[0] for word in duplicates): 
            country.sectors.remove(s)
    return country

    
##################################################
#               Main starts here                 #
##################################################
    
def splitPDFs(folder, output):
    try:
        # split first 2 pages of each country from folder gdata2020-04-10
        # Change name of folder if PDFs are in another folder
        paths = glob.glob(folder + '/*.pdf')
        if len(paths) != 0:
            if output != '' and os.path.isdir(output + '/'):
                for path in paths:
                    print(path)
                    pdf_splitter(path, output)
            else: print('Output folder does not exist. Please create an empty folder with that name or select an existing one.')
        else: print("Input folder is empty or does not exist")
        print('PDFs splitted!')
    except Exception as e: print(e)

def mergePDFs(path, output):
    try:
        # merge page 1 and 2 of each country and output them to folder PDFs
        if os.path.isdir(path + '/'):
            files = glob.glob(path+'/*.pdf') 
            sorted(files)
#            print('Number of countries:',len(files)/2)
            for page in range(0, len(files), 2):
                fileName = files[page].split("2020-")
                name = fileName[1][6:-5]
#                print(name)
                paths = glob.glob(path+'/*'+name+'*')
#                print(paths)
                name = output + "/" + name +".pdf"
                print(name)
                merger(name, paths)
            print("\nPDFs merged!")
        else:
            print('Empty or wrong folder')
    except Exception as e: print(e)

def convertToCSV(key, inputFolder, outputFolder):
    # Convert PDF to CSV with API
    try:
        import pdftables_api
        paths = glob.glob(inputFolder+'/*.pdf')
        if len(paths) == 0:
            print('Empty or wrong input folder')
            return
        for path in paths:
            name = outputFolder+path[len(inputFolder):-4]
            c = pdftables_api.Client(key)
            c.csv(path, name)
            print(name)
    except Exception as e: print(e)

def processCSVs(input_folder, output_name):
    if os.path.isdir(input_folder + '/'):
        paths = glob.glob(input_folder+'/*.csv')
        final = []
        for path in paths:
            dataset = readCSV(path)
            # Read only valuable information
            titles = ['Retail', 'Grocery', 'Parks', 'Transit', 'Work', 'Residential']
            country = CountryData()
            percentages = []
            i = 0
            while i < len(dataset):
                if len(dataset[i]) != 0:
    #                print(dataset[i])
    
                    #############################################
                    # Getcountry name - need to change this date#
                    #############################################
                    if 'April 5, 2020' in dataset[i][0]:
                        country.name = dataset[i][0]  + ' - ' + path[5:len(path)]
                        
                    # Get percentages
                    for item in dataset[i]:
                        if '%' in item or 'Not enough data' in item: 
                            if '\n' in item: percentages.append(item.split('\n')[0])
                            else: percentages.append(item)
                        
                    if any(word in dataset[i][0] for word in titles):
                        short = [[dataset[i][0]]]
#                        print(short)
                        for x in range(1, 15): # for the next 15 lines check if the section ends
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
                                # residential and parks are the last sectors in PDFs and sometimes they are not getting added 
                                if short[0][0] == 'Residential': 
                                    already_there = []
                                    for s in country.sectors: already_there.append(s.name.getSector()[0])
#                                    print('already_there:\t', already_there)
                                    if 'Residential' not in already_there: 
                                        sector = getValues(short)
                                        country.add_sector(sector)
                                if short[0][0] == 'Parks': 
                                    already_there = []
                                    for s in country.sectors: already_there.append(s.name.getSector()[0])
#                                    print('already_there:\t', already_there)
                                    if 'Parks' not in already_there: 
                                        sector = getValues(short)
                                        country.add_sector(sector)
                i += 1
            
            # Check for duplicates
            checkDuplicates(country)
            
            # Set Percentages and append to final list of countries
            percentages = getPercentage(percentages)
            for i in range(len(country.sectors)):
                country.sectors[i].name.percent = percentages[i]
            final.append(country)
                
        # Check for empty dates
        final = checkEmptyDates(final)
        
        # Order alphabetically by name
        final.sort(key=lambda x: x.name)
        
        # Print info to console
        for country in final:
            print(country.name)
            for sector in country.sectors:
                print('\t',sector.name.getSector())
    
        # Save to CSV file
        with open(output_name+'.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for country in final:
                writer.writerow([country.name])
                for i in range(len(country.sectors)):
                    space = ['']
                    for i in country.sectors[i].name.getSector():
                        space.append(i)
                    writer.writerow(space)
        print('\nInformation saved to file', output_name+'.csv')
        
    else: print('Input folder does not exist')