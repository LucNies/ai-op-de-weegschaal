# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 01:28:39 2015

@author: Tom
"""

from __future__ import division
import numpy as np
import random
import responder
import beta_utilities as beta_util
import util
import os

headers = [5]
adtypes = ['skyscraper', 'square']
colors = ['green', 'blue', 'red', 'white']
productids = np.arange(10, 26, 1)
prices = [10,15,20,25,30,35,40] 

pass_file = '../password.pass'
f = open(pass_file, 'rb')
teampw = f.next() 


#maak pagina's
possible_pages = beta_util.create_possible_pages(headers=headers, adtypes=adtypes, colors=colors, productids=productids, prices=prices) 

def train(iteration_rounds = 10, iterations = 20000, filename = 'training'):
    print 'starting training'
    
    alpha_list = []
    beta_list = []
    
    for q in range(1,iteration_rounds+1):
        alphas = np.ones(len(possible_pages))
        betas = np.ones(len(possible_pages))
        print 'Starting round ' + str(q)
        
        
        for i in range(0,iterations):
            randrunid = random.randint(0,9900)
            randi = random.randint(0,9000)
            page_index = beta_util.draw_from_beta_distributions(alphas=alphas, betas=betas, possible_pages = possible_pages) # welke arm wint
            
            bla = 0
            while bla<50:
                 try:
                     response = responder.respond_with_page(i=randi, runid=randrunid, page = possible_pages[page_index], teampw = teampw)
                 except Exception:
                     
                     bla = bla+1
                     continue
                 break
             
            success = response['effect']['Success'] # 1 of 0
            alphas, betas = beta_util.update_alphas_betas(index=page_index, success = success, price = possible_pages[page_index]['price'], alphas = alphas, betas = betas)
            util.update_progress(i/iterations)
            
        alpha_list.append(alphas)
        beta_list.append(betas)
        util.update_progress(1)
        print 'Round ' + str(q) + ' of ' + str(iteration_rounds) + ' finished.'
            
    alpha_list = np.array(alpha_list)
    beta_list = np.array(beta_list)
    
    final_alphas = alpha_list.mean(axis=0)
    final_betas = beta_list.mean(axis=0)
    beta_util.save_ab_to_filename(final_alphas, final_betas, filename)
    print 'training complete' 
    
if __name__ == '__main__':
    train()