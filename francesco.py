# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 23:40:14 2020

@author: Maria
"""

import os
import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
import csv

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
def getValues(string):
    values = ['']
    dates = []
    try:
        values.append(string[0][0])
        for x in string[3]:
            if x != '' and not (len(x) > 4):
                values.append(x)
        for x in string[-1]:
            if x != '':
                dates.append(x)
        values.append(dates[0])
        values.append(dates[2])
        return values
    except Exception as e:
        print(e)
        return values



if __name__ == '__main__':
    '''
    # split first 2 pages of each country from folder gdata2020-04-10
    paths = glob.glob('gdata2020-04-10/*.pdf')
    for path in paths:
        pdf_splitter(path)

    # merge page 1 and 2 of each country and output them to folder PDFs
    files = glob.glob('output/*.pdf')
    for page in range(0, len(files), 2):
        paths = [files[page], files[page+1]]
        name = "PDFs/" + files[page][18:35] +".pdf"
        print(name, paths)
        merger(name, paths)
    print("Success!")

    ###############################################
    # ONLY USE THIS PART ONCE AS THERE IS A LIMIT #
    ###############################################
    # Convert PDF to CSV with API - I reached my limit :/
    import pdftables_api
    paths = glob.glob('PDFs/*.pdf')
    for path in paths:
        print(path)
        name = 'PDFs/'+path[5:-4]
        print(name)
        c = pdftables_api.Client('9xlqz5nj7uh8')
        c.csv(path, name)

    '''

    # Read CSV files from folder PDFs
    paths = glob.glob('PDFs/*.csv')
    final = []
    for path in paths:
        dataset = []
        with open(path, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                dataset.append(row)

        # Read only valuable information
        titles = ['Retail', 'Grocery', 'Parks', 'Transit', 'Work', 'Residential']
        print("\n\n",dataset[1][0])
        final.append([dataset[1][0]])
        i = 0
        while i < len(dataset):
            if len(dataset[i]) != 0:
                if any(word in dataset[i][0] for word in titles):
                    short = [[dataset[i][0]]]
                    for x in range(1, 10):
                        try:
                            if any(word in dataset[i+x][0] for word in titles): break
                            else:
                                short.append(dataset[i+x])
                        except:
                            print("EOF")
                    for x in short:
                        print(x)
                    final.append(getValues(short))

            i += 1


    # Save info to a file
    with open('final.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(final)
