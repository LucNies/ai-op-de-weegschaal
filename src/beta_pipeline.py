# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 02:05:01 2015

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


util.update_progress(0)




def run(iterations = 350000, filename = '../data/alpha_beta/1.npz'):
	
	
	
	if not os.path.isfile(filename):
         
		alphas = np.ones(len(possible_pages))
		betas = np.ones(len(possible_pages))
		revenue = 0
	else:
		alphas, betas = beta_util.load_ab()
		revenue = util.load_profit()
	
	for i in range(0, iterations):
         
		
         randi = random.randint(0,10000)
         randrunid = random.randint(0,10000)
        		
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
         revenue = revenue + success*possible_pages[page_index]['price']
        		
         if i%100 == 0:
             beta_util.save_ab(alphas, betas)
             util.save_profit(revenue)
         util.update_progress(i/iterations)
		
	util.update_progress(1)
	
run()
    

