# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:55:42 2015

@author: Tom
"""

from __future__ import division
import numpy as np
from scipy.stats import beta
import os
import csv

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productids = np.arange(10, 26, 1)
prices = [10, 20, 30, 40, 50]



def create_possible_pages(headers, adtypes, colors, productids, prices):
    possible_pages=[]
    for header in headers:
        for adtype in adtypes:
            for color in colors:
                for productid in productids:
                    for price in prices:
                        possible_pages.append({'header': header, 'adtype' : adtype, 'color' : color, 'productid' : productid, 'price' : price})

    return possible_pages



def draw_from_beta_distributions(alphas, betas, possible_pages):

    max_id = 0
    max_=0
    
    for i in range(0, (alphas.size-1)):
        beta_outcome = float(beta.rvs(alphas[i], betas[i])*float(possible_pages[i]['price']/50))
        
        if  beta_outcome > max_:
            max_ = beta_outcome
            max_id = i
        
    return max_id
    
def update_alphas_betas(index, success, alphas, betas, price):
    
    if success==1:
        alphas[index] = float(alphas[index]+1)
        
    else:
        betas[index] = float(betas[index]+1)
        
    return alphas, betas
    
def save_ab(alphas, betas, file_path = '../data/alpha_beta/', i = 1):
      
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        filename = file_path + str(i)        

        np.savez(filename, alphas=alphas, betas=betas)

def save_ab_to_filename(alphas, betas, file_path = '../data/alpha_beta/', name = 'training'):
      
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        filename = file_path + name        

        np.savez(filename, alphas=alphas, betas=betas)

def load_ab(filename = '../data/alpha_beta/1.npz'):
   
    
    data = np.load(filename)
    a = data['alphas']
    b = data['betas']
    data.close()
    return a,b
    

    
if __name__ == '__main__':
    print 'hoi'

    
    
    
    
    
        
