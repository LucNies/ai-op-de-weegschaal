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

# aantal samples waar op getrained wordt
iterations = 10

#maak pagina's
possible_pages = beta_util.create_possible_pages(headers=headers, adtypes=adtypes, colors=colors, productids=productids, prices=prices) 

def train(runIds = 15):
    print 'starting training'
    
    run_ids_ran = []  
    alpha_list = []
    beta_list = []
    
    for q in range(1,runIds+1):
        alphas = np.ones(len(possible_pages))
        betas = np.ones(len(possible_pages))
        randrunid = random.randint(0,10000)
        
        while randrunid in run_ids_ran:
            randrunid = random.randint(0,10000)
        run_ids_ran.append(randrunid)
        
        for i in range(0,10000):
            page_index = beta_util.draw_from_beta_distributions(alphas=alphas, betas=betas, possible_pages = possible_pages) # welke arm wint
            
            bla = 0
            while bla<50:
                 try:
                     response = responder.respond_with_page(i=i, runid=randrunid, page = possible_pages[page_index], teampw = teampw)
                 except Exception:
                     
                     bla = bla+1
                     continue
                 break
             
            success = response['effect']['Success'] # 1 of 0
            alphas, betas = beta_util.update_alphas_betas(index=page_index, success = success, price = possible_pages[page_index]['price'], alphas = alphas, betas = betas)
            util.update_progress(i/10000)
            
        alpha_list.append(alphas)
        beta_list.append(betas)
        util.update_progress(1)
        print 'runId ' + str(q) + ' of ' + str(runIds) + ' finished.'
            
    alpha_list = np.array(alpha_list)
    beta_list = np.array(beta_list)
    
    final_alphas = alpha_list.mean(axis=0)
    final_betas = beta_list.mean(axis=0)
    beta_util.save_ab(final_alphas, final_betas)
    print 'training complete' 
    
if __name__ == '__main__':
    train()