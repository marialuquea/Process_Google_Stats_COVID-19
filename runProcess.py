# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:40:38 2020

@authors: Maria Luque Anguita and Francesco Pomponi

This file splits the PDFs from the folder gdata2020-4-10 and creates a new folder 'output' 
with all the 2-paged PDF of each country.

"""

import os
import glob
import csv
from PyPDF2 import PdfFileReader, PdfFileWriter
from country import CountryData, Sector

# split pages1 and 2 from every PDF
def pdf_splitter(path, output):
    try:
        fname = os.path.splitext(os.path.basename(path))[0]
        pdf = PdfFileReader(path)
        pdf_writer = PdfFileWriter()
        for page in range(2):
            pdf_writer.addPage(pdf.getPage(page))
        output_filename = output+'/{}_{}.pdf'.format(fname, page+1)
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename))
    except Exception as e: print(e)

# Get important values for each sector (retail, grocery...)
def getValues(short):
    # Name
    sector = Sector(short[0][0])
    
    dates = []
    months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ',
              'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
    # If any part in csv hasa month in it, add to dates list
    for x in short:
        for i in x:
            if any(word in i for word in months):
                if len(i) < 11: dates.append(i)
                else: dates.append(i[:10])
    try:
        # Dates - might be empty - get first and last 
        sector.startDate = dates[0]
        sector.endDate = dates[2]
        
    except: pass
    finally: return sector
    
    
def checkEmptyDates(final):
    try:
        # If any sector in the country has a date, make a copy of it in date1 and date2
        for country in final:
            date1 = ''
            date2 = ''
            for sector in country.sectors:
                if sector.name.startDate != '': date1 = sector.name.startDate
                if sector.name.endDate != '': date2 = sector.name.endDate
            # loop again to check if any of the sector dates are empty and set them from date1 and date2
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
    # loop starting at 0, until the end of list, in steps of 5
    # because every sector has 5 percentages: +80%, +40%, the one we want, -40% and -80%
    for i in range(0, len(percentages), 5):
        short = []
        for j in range(5):
            short.append(percentages[i+j]) #add those 5 to list short
        percent_set = set(short) 
        '''             make it a set - no repeated elements - 
        therefore if there are two 40s or 80s, the set will have a length of 4
        if the percentage is different to 40 or 80, the set will have a length of 5   '''
        if len(percent_set) == 5: # if percentage is not 40% or 80%
            percentage = [ x for x in percent_set if "40" not in x and '80' not in x][0]
        else: # if percentage is either 40 or 80
            if short.count('+80%') == 2: percentage = '+80%'
            if short.count('-80%') == 2: percentage = '-80%'
            if short.count('+40%') == 2: percentage = '+40%'
            if short.count('-40%') == 2: percentage = '-40%'
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
    # add all sectors to list, even if sector was added twice
    for s in country.sectors: already_there.append(s.name.getSector()[0])
    # check if sector was added twice and add name to duplicates list
    for s in already_there: 
        if already_there.count(s) > 1: duplicates.append(s)
    # loop through sectors in country, if the sector's name appears in duplicates, remove 1
    for s in country.sectors:
        if any(word in s.name.getSector()[0] for word in duplicates): 
            country.sectors.remove(s)
    return country

    
##################################################
#               Main starts here                 #
##################################################
    
def splitPDFs(folder, output):
    try:
        # Make a list of all the PDF files in the specified folder
        paths = glob.glob(folder + '/*.pdf')
        print ("split PDFs count:", len(paths))
        
        # If folder is not empty
        if len(paths) != 0:
            
            # If output is not empty (where the PDFs will go) AND the directory exists
            if output != '' and os.path.isdir(output + '/'):
                
                for path in paths: # For each PDF
                    pdf_splitter(path, output) # Split PDFs
                print('PDFs splitted!')
                
            else: print('Output folder does not exist. Please create an empty folder with that name or select an existing one.')
        else: print("Input folder is empty or does not exist")
        
    except Exception as e: print(e)



def convertToCSV(key, inputFolder, outputFolder):
    # Convert PDF to CSV with API
    try:
        import pdftables_api
        
        # Make a list of all PDF files in input folder
        paths = glob.glob(inputFolder+'/*.pdf')
        print("CSVs count:", len(paths))
        
        if len(paths) == 0:
            print('Empty or wrong input folder')
            return
        
        for path in paths:
            # Name is output folder plus name of file minus last 4 characters '.pdf'
            name = outputFolder+path[len(inputFolder):-4]
            c = pdftables_api.Client(key)
            c.csv(path, name)
            print(name)
            
    except Exception as e: print(e)



def processCSVs(input_folder, output_name):
    # if directory exists
    if os.path.isdir(input_folder + '/'):
        
        # make a list of all CSV files in input folder
        paths = glob.glob(input_folder+'/*.csv')
        final = []
        
        for path in paths:
            
            #read CSV
            dataset = readCSV(path)
            
            # Make an empty country object from class CountryData
            country = CountryData()
            
            # In some files, the second line is the name, in others it is an 80, if not 80, set as country name
            country.name = dataset[1][0] + ' - ' + path[5:len(path)]
            
            percentages = []
            i = 0
            while i < len(dataset): #loop through every line of CSV
                
                # if line is not empty
                if len(dataset[i]) != 0:
                    
                    # Get percentages
                    for item in dataset[i]:
                        if '%' in item or 'Not enough data' in item: 
                            if '\n' in item: percentages.append(item.split('\n')[0])
                            else: percentages.append(item)
                    
                    # Get sector name
                    titles = ['Retail', 'Grocery', 'Parks', 'Transit', 'Work', 'Residential']
                    if any(word in dataset[i][0] for word in titles):
                        short = [[dataset[i][0]]]
                        
                        # for the next 15 lines check if the sector ends
                        for x in range(1, 15): 
                            try:
                                # when sector is complete (another sector word is found)
                                if any(word in dataset[i+x][0] for word in titles): 
                                    sector = getValues(short)
                                    country.add_sector(sector)
                                    break
                                
                                else: # keep adding info to sector until complete
                                    short.append(dataset[i+x])
                            except: 
                                # residentialis the last sectors in PDFs and sometimes it doesn't get added
                                if short[0][0] == 'Residential': 
                                    already_there = []
                                    for s in country.sectors: already_there.append(s.name.getSector()[0])
                                    if 'Residential' not in already_there: 
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