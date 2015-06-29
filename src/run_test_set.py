# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 00:36:34 2015

@author: Tom
"""

from __future__ import division
import numpy as np
import random
import responder
import beta_utilities as beta_util
import util
import os

headers = [5,15]
adtypes = ['skyscraper', 'square']
colors = ['green', 'blue', 'red', 'white']
productids = np.arange(10, 21, 1)
prices = [15,20,25,30,40,50] 

pass_file = '../password.pass'
f = open(pass_file, 'rb')
teampw = f.next() 


#maak pagina's
possible_pages = beta_util.create_possible_pages(headers=headers, adtypes=adtypes, colors=colors, productids=productids, prices=prices) 

def test_model(ab_path = '../data/alpha_beta/training.npz'):
    print 'starting training'
    alphas,betas = beta_util.load_ab(filename=ab_path)
    for q in range(10001,10101):
       
        print 'Starting runId ' + str(q)
        runid = q
        revenue = 0
        
        for i in range(0,10001):
            
            page_index = beta_util.draw_from_beta_distributions(alphas=alphas, betas=betas, possible_pages = possible_pages) # welke arm wint
            
            bla = 0
            while bla<50:
                 try:
                     response = responder.respond_with_page(i=i, runid=runid, page = possible_pages[page_index], teampw = teampw)
                 except Exception:
                     
                     bla = bla+1
                     continue
                 break
             
            success = response['effect']['Success'] # 1 of 0
            revenue = revenue + success*possible_pages[page_index]['price']            
            
            alphas, betas = beta_util.update_alphas_betas(index=page_index, success = success, price = possible_pages[page_index]['price'], alphas = alphas, betas = betas)
            util.update_progress(i/10001)
            
        util.save_profit(revenue)
        beta_util.save_ab(alphas, betas)
        
        util.update_progress(1)
        print 'RunId ' + str(q) + ' of ' + str(10100) + ' finished.'
            
    beta_util.save_ab_to_filename(alphas, betas, name='testing')
    print 'training complete' 
    
if __name__ == '__main__':
    #test_model() #gecomment zodat hij niet per ongelijk een keer start.
    print 'fk u dolphin!'