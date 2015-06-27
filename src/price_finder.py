# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:04:13 2015

@author: Luc
"""

from __future__ import division
from scipy.stats import beta
import numpy as np
import util
import beta_utilities as beta_util
import random

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productids = np.arange(10, 26, 1)
prices = np.arange(5, 51, 5)


class PriceFinder(object):
	
	def __init__(self, first_time = True, pass_file = '../password.pass'):
		f = open(pass_file, 'rb')
		self.teampw = f.next()
		f.close()
		
		if first_time:
			self.create_alpha_beta()
			self.revenue = 0
		else:
			self.load_ab()
			self.revenue = util.load_profit()
	
	
	def create_alpha_beta():
		self.product_price_alpha = np.ones(len(productids), len(prices)) 
		self.product_price_beta = np.ones(len(productids), len(prices)) 
		
	def give_page():
		
		product = random.randint(0, len(productids)-1)
		prod_price_dist = beta.rvs(self.product_price_alpha[product])
		
		
	