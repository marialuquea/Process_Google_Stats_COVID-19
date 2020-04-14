# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:26:03 2020

@author: Maria
"""

from runProcess import mergePDFs, splitPDFs, convertToCSV, processCSVs
import subprocess

def ask():
    print("\nWhat do you want to do?")
    print("1 - Download all PDFs from Google")
    print("2 - Split PDFs to get first 2 pages")
    print("3 - Merge 2 pages of each PDF")
    print("4 - Convert PDFs to CSVs")
    print("5 - Process CSVs")
    print("6 - Exit")
    
    number = 0
    acceptedOption = False
    while acceptedOption is False:
        try:
            number = int(input("Select number: "))
        except:
            print('Invalid input, select a number (1 to 6)')
            break
        if number > 0 and number < 7:
            acceptedOption = True
        else:
            print("Invalid number, select a number (1 to 6)")
            
    if number == 1: 
        print('\nGetting PDFs from Google...')
        process = subprocess.Popen(['downloadPDFs.sh'])
        process.wait() # Wait for process to complete.
        # iterate on the stdout line by line
        for line in process.stdout.readlines():
            print(line)
            
    if number == 2: 
        folder = input('Name of folder where PDFs to be converted are: ')
        print('\nSplitting PDFs to get the first 2 pages...')
#        splitPDFs(folder)
    if number == 3: 
        print('\nMerging PDFs...')
#        mergePDFs()
    if number == 4: 
        key = input('API personal key to use: ')
        print('Converting to CSV...')
#        convertToCSV(key)
    if number == 5: 
        output_name = input('What do you want to name the output file?: ')
        print('Processing CSV files...')
#        processCSVs(output_name)

    return number

if __name__ == '__main__':
    
    # Print initial title of program
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print (f.renderText('COVID-19 Google Stats Processor'))
    
    finished = False
    number = 0
    while finished == False:
        number = ask()
        if number == 6:
            print("\n\tBYE BYE")
            break
    
    
        
    
        
        
        
    