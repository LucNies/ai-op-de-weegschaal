# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:04:13 2015

@author: Luc
"""

from __future__ import division
from scipy.stats import beta
import numpy as np
import util
import responder
import random
import os
import csv
from context_getter import ContextGetter

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square']
colors = ['green', 'blue', 'red', 'white']
productids = np.arange(10, 26, 1)
prices = np.arange(5, 51, 5)


class PriceFinder(object):
	
	def __init__(self, first_time = True, pass_file = '../password.pass'):
		f = open(pass_file, 'rb')
		self.contextGetter = ContextGetter(0)
		self.teampw = f.next()
		f.close()
		
		if first_time:
			self.create_alpha_beta()
			self.revenue = 0
		else:
			self.load_ab()
			self.revenue = util.load_profit()
	
	
	def create_alpha_beta(self) :
		
		self.product_alpha = np.ones(len(productids))
		self.product_beta = np.ones(len(productids))
	
		
		self.product_price_alpha = np.ones((len(productids), len(prices)))
		self.product_price_beta = np.ones((len(productids), len(prices)))
	
		self.header_alpha= np.ones(len(headers))
		self.header_beta = np.ones(len(headers))
		
		self.adtype_alpha = np.ones(len(adtypes))
		self.adtype_beta = np.ones(len(adtypes))
		
		self.color_alpha = np.ones(len(colors))
		self.color_beta = np.ones(len(colors))		
	
	def give_page(self):
		
		#get product
		product_i = random.randint(0, len(productids)-1)
		product = productids[product_i]
		
		#get price
		prod_price_dist = beta.rvs(self.product_price_alpha[product_i], self.product_price_beta[product_i])*(prices/50.0)
		price_i = np.argmax(prod_price_dist)
		price = prices[price_i]
		
		
		#get header
		header_dist = beta.rvs(self.header_alpha, self.header_beta)
		header_i = np.argmax(header_dist)
		header = headers[header_i]
		
		#get adtype
		adtype_dist = beta.rvs(self.adtype_alpha, self.adtype_beta)
		adtype_i = np.argmax(adtype_dist)
		adtype = adtypes[adtype_i]
		
		#get color
		color_dist = beta.rvs(self.color_alpha, self.color_beta)
		color_i = np.argmax(color_dist)
		color = colors[color_i]
		

		
		return {'header': header, 'adtype': adtype, 'color': color, 'productid': product, 'price': price}, [header_i, adtype_i, color_i, product_i, price_i]
			
		
	def save_ab(self, file_path = '../data/alpha_beta/'):
		
		if not os.path.exists(file_path):
	            os.makedirs(file_path)
													
		filename = file_path + "pricechecker_ab_new_scaled"											
		
		np.savez(filename, 
		header_alpha = self.header_alpha,
		adtype_alpha = self.adtype_alpha,
		color_alpha = self.color_alpha,
		product_alpha = self.product_alpha,
		product_price_alpha = self.product_price_alpha,
		
		header_beta = self.header_beta,
		adtype_beta = self.adtype_beta,
		color_beta = self.color_beta,
		product_beta = self.product_beta,
		product_price_beta = self.product_price_beta
		)
	
	def load_ab(self, filename = '../data/alpha_beta/pricechecker_ab_new_scaled.npz'):
		
		data = np.load(filename)
		
		self.header_alpha = data['header_alpha']
		self.adtype_alpha = data['adtype_alpha']
		self.color_alpha = data['color_alpha']
		self.product_alpha = data['product_alpha']
		self.product_price_alpha = data['product_price_alpha']
		
		self.header_beta = data['header_beta']		
		self.adtype_beta = data['adtype_beta']
		self.color_beta = data['color_beta']
		self.product_beta = data['product_beta']
		self.product_price_beta = data['product_price_beta']	
		
		data.close()
		
		
	def update_alpha_betas(self, succes, indexes):

		price = prices[indexes[4]]
		if succes:
			self.header_alpha[indexes[0]] += 1#float(1*price/50)
			self.adtype_alpha[indexes[1]] += 1#float(1*price/50)
			self.color_alpha[indexes[2]] += 1#float(1*price/50)
			self.product_alpha[indexes[3]] += 1#float(1*price/50)
			self.product_price_alpha[indexes[3]][indexes[4]] += 1#float(1*price/50)
			
		else:
			self.header_beta[indexes[0]] += 1#float(1*price/50)
			self.adtype_beta[indexes[1]] += 1#float(1*price/50)
			self.color_beta[indexes[2]] += 1#float(1*price/50)
			self.product_beta[indexes[3]] += 1#float(1*price/50)
			self.product_price_beta[indexes[3]][indexes[4]] += 1#float(1*price/50)
		

	def run(self, iterations = 400000):
		
		
		for i in range(0, iterations):
			
			randi = random.randint(0,9900)
			randrunid = random.randint(0,10000)
			page, pageindex = self.give_page()# welke arm wint
			response = responder.respond_with_page(i=randi, runid=randrunid, page = page, teampw = self.teampw)
			
			success = response['effect']['Success'] # 1 of 0
			
			self.update_alpha_betas(success, pageindex)

			self.revenue += success*page['price']
			
			if i%10 == 0:
				self.save_ab()
#				util.save_profit(self.revenue)
			
			util.update_progress(i/iterations)
			
		util.update_progress(1)	

	def inspect_prices(self):
		
		dist = self.product_price_alpha/self.product_price_beta
		dist1 = self.product_price_alpha[0]/self.product_price_beta[0]
		
		with open("../data/product_price_dist_new_scaled.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(dist)
		f.close()
		
			
		
			
		
if __name__ == "__main__":
	priceFinder = PriceFinder(first_time = True)
	priceFinder.run()
	priceFinder.inspect_prices()
	
		