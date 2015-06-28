# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 20:19:04 2015

@author: Luc
"""
from __future__ import division
import numpy as np
from scipy.stats import beta
import os
import util
import random
import util
import responder

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productids = np.arange(10, 26, 1)
prices = np.array([25,35,45])

class IndependentTrainer(object):
	
	def __init__(self, first_timer = True, pass_file = '../password.pass'):
		f = open(pass_file, 'rb')
		self.teampw = f.next()
		f.close()
		
		if first_timer:
			self.create_aplha_beta()
			self.revenue = 0
		else:
			self.load_ab()
			self.revenue = util.load_profit()
	
	def create_aplha_beta(self):
		self.header_alpha= np.ones(len(headers))
		self.header_beta = np.ones(len(headers))
		
		self.adtype_alpha = np.ones(len(adtypes))
		self.adtype_beta = np.ones(len(adtypes))
		
		self.color_alpha = np.ones(len(colors))
		self.color_beta = np.ones(len(colors))
		
		self.product_alpha = np.ones(len(productids))
		self.product_beta = np.ones(len(productids))
		
		self.price_alpha = np.ones(len(prices))
		self.price_beta = np.ones(len(prices))
	
	def give_page(self):
		
		#get header
		header_dist = [beta.rvs(self.header_alpha[i], self.header_beta[i]) for i in range(len(headers))]
		header_i = header_dist.index(max(header_dist))
		header = headers[header_i]
		
		#get adtype
		adtype_dist = [beta.rvs(self.adtype_alpha[i], self.adtype_beta[i]) for i in range(len(adtypes))]
		adtype_i = adtype_dist.index(max(adtype_dist))
		adtype = adtypes[adtype_i]
		
		#get color
		color_dist = [beta.rvs(self.color_alpha[i], self.color_beta[i]) for i in range(len(colors))]
		color_i = color_dist.index(max(color_dist))
		color = colors[color_i]
		
		#get productid
		product_dist = [beta.rvs(self.product_alpha[i], self.product_beta[i]) for i in range(len(productids))]
		product_i = product_dist.index(max(product_dist))
		product = productids[product_i]

		#get price
		price_dist = [beta.rvs(self.price_alpha[i], self.price_beta[i]) for i in range(len(prices))]*(prices/50.0)
		price_i = price_dist.index(max(price_dist))
		price = prices[price_i]		
		
		return {'header': header, 'adtype': adtype, 'color': color, 'productid': product, 'price': price}, [header_i, adtype_i, color_i, product_i, price_i]
	
	def update_alpha_betas(self, succes, indexes):

		price = prices[indexes[4]]
		if succes:
			self.header_alpha[indexes[0]] += 1
			self.adtype_alpha[indexes[1]] += 1
			self.color_alpha[indexes[2]] += 1
			self.product_alpha[indexes[3]] += 1
			self.price_alpha[indexes[4]] += 1
			
		else:
			self.header_beta[indexes[0]] += 1
			self.adtype_beta[indexes[1]] += 1
			self.color_beta[indexes[2]] += 1
			self.product_beta[indexes[3]] += 1
			self.price_beta[indexes[4]] += 1
		
	def save_ab(self, file_path = '../data/alpha_beta/'):
		
		if not os.path.exists(file_path):
	            os.makedirs(file_path)
													
		filename = file_path + "independent_ab"											
		
		np.savez(filename, 
		header_alpha = self.header_alpha,
		adtype_alpha = self.adtype_alpha,
		color_alpha = self.color_alpha,
		product_alpha = self.product_alpha,
		price_alpha = self.price_alpha,
		
		header_beta = self.header_beta,
		adtype_beta = self.adtype_beta,
		color_beta = self.color_beta,
		product_beta = self.product_beta,
		price_beta = self.price_beta
		)
	
	def load_ab(self, filename = '../data/alpha_beta/independent_ab.npz'):
		
		data = np.load(filename)
		
		self.header_alpha = data['header_alpha']
		self.adtype_alpha = data['adtype_alpha']
		self.color_alpha = data['color_alpha']
		self.product_alpha = data['product_alpha']
		self.price_alpha = data['price_alpha']

		self.header_beta = data['header_beta']
		
		self.adtype_beta = data['adtype_beta']
		self.color_beta = data['color_beta']
		self.product_beta = data['product_beta']
		self.price_beta = data['price_beta']	
		
		data.close()
	
	def run(self, iterations = 200000):
		
		
		for i in range(0, iterations):
			
			randi = random.randint(0,10000)
			randrunid = random.randint(0,10000)
			
			page, pageindex = self.give_page()# welke arm wint
			response = responder.respond_with_page(i=randi, runid=randrunid, page = page, teampw = self.teampw)
			
			success = response['effect']['Success'] # 1 of 0
			
			self.update_alpha_betas(success, pageindex)

			self.revenue += success*page['price']
			
			if i%10 == 0:
				self.save_ab()
				util.save_profit(self.revenue)
			
			util.update_progress(i/iterations)
			
		util.update_progress(1)		
					


if __name__ == '__main__':
	trainer = IndependentTrainer(first_timer = True)
	trainer.run()

