# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 09:28:59 2020

@author: Maria
"""

class Sector(object):
    def __init__(self, name):
        self.name = name
        self.percent = ''
        self.startDate = ''
        self.endDate = ''
        
    def getSector(self):
        sector = [self.name, self.percent, self.startDate, self.endDate]
        return sector
    

class CountryData(object):
    def __init__(self):
        
        self.name = ''
        self.sectors = []
        
    def add_sector(self, sector):
        self.sectors.append(Sector(sector))
        
      
    
    
