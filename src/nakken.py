# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:55:42 2015

@author: Tom
"""

import numpy as np
import json
from scipy.stats import beta

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productids = np.arange(10, 26, 1)
price = 25

possible_pages=[]

for header in headers:
    for adtype in adtypes:
        for color in colors:
            for productid in productids:
                possible_pages.append({'header': header, 'adtype' : adtype, 'color' : color, 'productid' : productid})


print len(possible_pages)
