# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:55:42 2015

@author: Tom
"""

import numpy as np
import json
import responder
from scipy.stats import beta

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productids = np.arange(10, 26, 1)
price = 25



def create_possible_pages(headers, adtypes, colors, productids, price):
    possible_pages=[]
    for header in headers:
        for adtype in adtypes:
            for color in colors:
                for productid in productids:
                    possible_pages.append({'header': header, 'adtype' : adtype, 'color' : color, 'productid' : productid, 'price' : price})

    return possible_pages



def draw_from_beta_distributions(alphas, betas):

    max_id = 0
    for i in range(0, (len(alphas)-1)):
        if beta.rvs(alphas[i], betas[i]) > max_id:
            max_id = i
        
    return i
    
def update_alphas_betas(index, success, alphas, betas):
    
    if success:
        alphas[index] = alphas[index]+1
    else:
        betas[index] = betas[index]+1
    
    return alphas, betas
    
if __name__ == '__main__':
    
    headers = [5, 15, 35]
    adtypes = ['skyscraper', 'square', 'banner']
    colors = ['green', 'blue', 'red', 'black', 'white']
    productids = np.arange(10, 26, 1)
    price = 25   

    possible_pages = create_possible_pages(headers=headers, adtypes=adtypes, colors=colors, productids=productids, price=price) 
    print len(possible_pages)
    
    
    
    
        
