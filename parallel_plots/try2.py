# -*- coding: utf-8 -*-
"""
Created on Sat May  9 09:13:16 2020

@author: Maria
"""


import pandas
import matplotlib.pyplot as plt
from pandas.tools.plotting import parallel_coordinates

data = pandas.read_csv(r'C:\Python27\Lib\site-packages\pandas\tests\data\iris.csv', sep=',')
parallel_coordinates(data, 'Name')
plt.show()