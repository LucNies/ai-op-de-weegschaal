# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:55:42 2015

@author: Tom
"""

from __future__ import division
import numpy as np
from scipy.stats import beta

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productids = np.arange(10, 26, 1)
prices = [25,35,45]



def create_possible_pages(headers, adtypes, colors, productids, prices):
    possible_pages=[]
    for header in headers:
        for adtype in adtypes:
            for color in colors:
                for productid in productids:
                    for price in prices:
                        possible_pages.append({'header': header, 'adtype' : adtype, 'color' : color, 'productid' : productid, 'price' : price})

    return possible_pages



def draw_from_beta_distributions(alphas, betas):

    max_id = 0
    max_=0
    
    for i in range(0, (alphas.size-1)):
        beta_outcome = beta.rvs(alphas[0,i], betas[0,i])
        
        if  beta_outcome > max_:
            max_ = beta_outcome
            max_id = i
        
    return max_id
    
def update_alphas_betas(index, success, alphas, betas, price):
    
    if success==1:
        alphas[0,index] = float(alphas[0,index]+1*(price/50))# pas alpha aan naar de prijs van het product
        
    else:
        betas[0,index] = float(betas[0,index]+1*(price/50))# niet zeker of het bij de failures ook moet
        
    return alphas, betas
    
if __name__ == '__main__':
    
    headers = [5, 15, 35]
    adtypes = ['skyscraper', 'square', 'banner']
    colors = ['green', 'blue', 'red', 'black', 'white']
    productids = np.arange(10, 26, 1)
    price = 25   

    possible_pages = create_possible_pages(headers=headers, adtypes=adtypes, colors=colors, productids=productids, price=price) 
    print len(possible_pages)
    
    
    
    
        
