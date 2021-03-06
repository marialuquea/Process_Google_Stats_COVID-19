# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:26:03 2020

@author: Maria Luque Anguita
"""

from runProcess import splitPDFs, convertToCSV, processCSVs
import subprocess

def ask():
    print("\nWhat do you want to do?")
    print("1 - Download all PDFs from Google")
    print("2 - Split PDFs to get first 2 pages")
    print("3 - Convert PDFs to CSVs")
    print("4 - Process CSVs")
    print("5 - Exit")
    
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
        sh = subprocess.Popen1(["bash", "downloadPDFs.sh"])
        sh.wait()   
        print('All PDFs downloaded!')
           
    if number == 2: 
        folder = input('Input folder (where PDFs to be converted are): ')
        output = input('Output folder (where PDFs will appear): ')
        splitPDFs(folder, output)

    if number == 3:
        print("\nUncomment lines 175 and 176 in runProcess.py for this to work. If you don't uncomment them, it will look as if it does work, but it actually doesn't haha.")
        key = input('API personal key to use: ')
        inputFolder = input('Input folder (where merged PDFs are located):')
        outputFolder = input('Output folder (where CSVs will go - this folder must already exist):')
        convertToCSV(key, inputFolder, outputFolder)
        
    if number == 4: 
        input_dir = input('Input folder (where CSVs are): ')
        output_name = input('What do you want to name the output file?: ')
        print('\nProcessing CSV files...')
        processCSVs(input_dir, output_name)

    return number

if __name__ == '__main__':
    
    # Print initial title of program
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print (f.renderText('COVID-19 Google Stats Processor'))
    
    # Loop the questions until the user selects option 6 (exit)
    while True:
        number = ask()
        if number == 5:
            print("\n\tBYE BYE")
            break
    
    
        
    
        
        
        
    