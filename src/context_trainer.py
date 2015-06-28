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
import json
from context_getter import ContextGetter

headers = [5, 35]
adtypes = ['skyscraper', 'square']
colors = ['green', 'blue', 'red', 'white']
productids = np.arange(10, 26, 1)
prices = np.arange(5, 51, 5)
import pickle

class ContextTrainer(object):
	
	def __init__(self, first_timer = True, pass_file = '../password.pass'):
		f = open(pass_file, 'rb')
		self.teampw = f.next()
		f.close()
		self.contextGetter = ContextGetter(0)
		if first_timer:
			self.create_aplha_beta()
			self.revenue = 0
		else:
			self.load_ab()
			self.revenue = util.load_profit()
	
	def create_aplha_beta(self):
		
		#productid, product-price, headers, adtypes, colors		
		windows_ab = [
		[
		np.ones(len(productids)),
		np.ones(len(productids))
		],
		[
		np.ones((len(productids), len(prices))),
		np.ones((len(productids), len(prices)))
		],
		[
		np.ones(len(headers)),
		np.ones(len(headers))
		],
		[
		np.ones(len(adtypes)),
		np.ones(len(adtypes))
		],
		[
		np.ones(len(colors)),
		np.ones(len(colors))		
		]
		]
		
		linux_ab = [
		[
		np.ones(len(productids)),
		np.ones(len(productids))
		],
		[
		np.ones((len(productids), len(prices))),
		np.ones((len(productids), len(prices)))
		],
		[
		np.ones(len(headers)),
		np.ones(len(headers))
		],
		[
		np.ones(len(adtypes)),
		np.ones(len(adtypes))
		],
		[
		np.ones(len(colors)),
		np.ones(len(colors))		
		]
		]
		
		OSX_ab = [
		[
		np.ones(len(productids)),
		np.ones(len(productids))
		],
		[
		np.ones((len(productids), len(prices))),
		np.ones((len(productids), len(prices)))
		],
		[
		np.ones(len(headers)),
		np.ones(len(headers))
		],
		[
		np.ones(len(adtypes)),
		np.ones(len(adtypes))
		],
		[
		np.ones(len(colors)),
		np.ones(len(colors))		
		]
		]
		
		
		mobile_ab = [
		[
		np.ones(len(productids)),
		np.ones(len(productids))
		],
		[
		np.ones((len(productids), len(prices))),
		np.ones((len(productids), len(prices)))
		],
		[
		np.ones(len(headers)),
		np.ones(len(headers))
		],
		[
		np.ones(len(adtypes)),
		np.ones(len(adtypes))
		],
		[
		np.ones(len(colors)),
		np.ones(len(colors))		
		]
		]
		
		self.agent_ab = {'OSX':OSX_ab, 'Windows':windows_ab, 'Linux': linux_ab, 'mobile': mobile_ab}	
		
	def give_page(self, context):
		
		product_alpha, product_beta, product_price_alpha, product_price_beta, header_alpha, header_beta, adtype_alpha, adtype_beta, color_alpha, color_beta = self.get_context_ab(context)
		
		header_dist = [beta.rvs(header_alpha[i], header_beta[i]) for i in range(len(headers))]
		header_i = header_dist.index(max(header_dist))
		header = headers[header_i]
		
		#get adtype
		adtype_dist = [beta.rvs(adtype_alpha[i], adtype_beta[i]) for i in range(len(adtypes))]
		adtype_i = adtype_dist.index(max(adtype_dist))
		adtype = adtypes[adtype_i]
		
		#get color
		color_dist = [beta.rvs(color_alpha[i], color_beta[i]) for i in range(len(colors))]
		color_i = color_dist.index(max(color_dist))
		color = colors[color_i]
		
		#get productid
		product_dist = [beta.rvs(product_alpha[i], product_beta[i]) for i in range(len(productids))]
		product_i = product_dist.index(max(product_dist))
		product = productids[product_i]

		#get price
		price_alpha = product_price_alpha[product_i]
		price_beta = product_price_beta[product_i]
		price_dist = [beta.rvs(price_alpha[i], price_beta[i]) for i in range(len(prices))]
		price_i = price_dist.index(max(price_dist))
		price = prices[price_i]		
		
		return {'header': header, 'adtype': adtype, 'color': color, 'productid': product, 'price': price}, [product_i, price_i, header_i, adtype_i, color_i]
	
	def get_context_ab(self, context):
		
		agent = str(context['Agent'])
		agent_pages = self.agent_ab[agent]		

		#get productids
		product_alpha = agent_pages[0][0]
		product_beta = agent_pages[0][1]		
		
		#get_price
		prod_price_alpha = agent_pages[1][0]
		prod_price_beta = agent_pages[1][1]
				
		#get header
		header_alpha = agent_pages[2][0]
		header_beta = agent_pages[2][1]
		
		#get adtype
		adtype_alpha = agent_pages[3][0]
		adtype_beta = agent_pages[3][1]
		
		#get color
		color_alpha = agent_pages[4][0]
		color_beta = agent_pages[4][0]
		
		return product_alpha, product_beta, prod_price_alpha, prod_price_beta, header_alpha, header_beta, adtype_alpha, adtype_beta, color_alpha, color_beta
		
	
	
	def update_alpha_betas(self, succes, indexes, context):

		agent = context['Agent']
		if succes:
			self.agent_ab[agent][0][0][indexes[0]] += 1#product
			self.agent_ab[agent][1][0][indexes[1]] += 1#price
			self.agent_ab[agent][2][0][indexes[2]] += 1#header
			self.agent_ab[agent][3][0][indexes[3]] += 1#adtype
			self.agent_ab[agent][4][0][indexes[4]] += 1#color
			
		else:
			self.agent_ab[agent][0][1][indexes[0]] += 1#product
			self.agent_ab[agent][1][1][indexes[1]] += 1#price
			self.agent_ab[agent][2][1][indexes[2]] += 1#header
			self.agent_ab[agent][3][1][indexes[3]] += 1#adtype
			self.agent_ab[agent][4][1][indexes[4]] += 1#color
		
	def save_ab(self, file_path = '../data/alpha_beta/'):
		
		pickle.dump(self.agent_ab, open(file_path + "agent_ab.p", 'wb'))
		
#		if not os.path.exists(file_path):
#	            os.makedirs(file_path)
#													
#		filename = file_path + "independent_ab"											
#		
#		np.savez(filename, 
#		header_alpha = self.header_alpha,
#		adtype_alpha = self.adtype_alpha,
#		color_alpha = self.color_alpha,
#		product_alpha = self.product_alpha,
#		price_alpha = self.price_alpha,
#		
#		header_beta = self.header_beta,
#		adtype_beta = self.adtype_beta,
#		color_beta = self.color_beta,
#		product_beta = self.product_beta,
#		price_beta = self.price_beta
#		)
	
	def load_ab(self, filename = '../data/alpha_beta/agent_ab.p'):
		
		self.agent_ab = pickle.load(open(filename,'rb'))		
		
#		data = np.load(filename)
#		
#		self.header_alpha = data['header_alpha']
#		self.adtype_alpha = data['adtype_alpha']
#		self.color_alpha = data['color_alpha']
#		self.product_alpha = data['product_alpha']
#		self.price_alpha = data['price_alpha']
#
#		self.header_beta = data['header_beta']
#		
#		self.adtype_beta = data['adtype_beta']
#		self.color_beta = data['color_beta']
#		self.product_beta = data['product_beta']
#		self.price_beta = data['price_beta']	
#		
#		data.close()
	
	def run(self, iterations = 200000):
		
		
		for i in range(0, iterations):
			
			randi = random.randint(0,10000)
			randrunid = random.randint(0,10000)
			context = self.contextGetter.call(randi, randrunid)
			page, pageindex = self.give_page(context)# welke arm wint
			response = responder.respond_with_page(i=randi, runid=randrunid, page = page, teampw = self.teampw)
			
			success = response['effect']['Success'] # 1 of 0
			
			self.update_alpha_betas(success, pageindex, context)

			self.revenue += success*page['price']
			
			if i%1000 == 0:
				self.save_ab()
				util.save_profit(self.revenue)
			
			util.update_progress(i/iterations)
			
		util.update_progress(1)		
					


if __name__ == '__main__':
	trainer = ContextTrainer(first_timer = True)
	trainer.run()

