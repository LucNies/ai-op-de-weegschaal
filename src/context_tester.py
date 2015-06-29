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
from copy import deepcopy
import csv

headers = [5, 15]
adtypes = ['skyscraper', 'square']
colors = ['green', 'blue', 'red', 'white']
productids = np.arange(10, 21, 1)
prices = np.arange(5, 51, 5)
import pickle

class ContextTrainer(object):
	
	def __init__(self, modelid, first_timer = True, pass_file = '../password.pass'):
		f = open(pass_file, 'rb')
		self.teampw = f.next()
		self.modelid = modelid
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
		ab_matrix = [
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
		
		#agent context
		windows_ab = deepcopy(ab_matrix)		
		linux_ab = deepcopy(ab_matrix)		
		OSX_ab = deepcopy(ab_matrix)
		mobile_ab = deepcopy(ab_matrix)
		
		#age context
		under20_ab = deepcopy(ab_matrix)
		from20till30_ab = deepcopy(ab_matrix)
		from30till40_ab = deepcopy(ab_matrix)
		from40till60_ab = deepcopy(ab_matrix)
		from60older_ab =deepcopy(ab_matrix)
		
		#language context
		eng_ab = deepcopy(ab_matrix)
		nl_ab = deepcopy(ab_matrix)
		ger_ab = deepcopy(ab_matrix)
		
		google_ab = deepcopy(ab_matrix)
		bing_ab = deepcopy(ab_matrix)
		na_ab = deepcopy(ab_matrix)
		

		self.age_ab = {'young': under20_ab, 'young_adult': from20till30_ab, 'adult': from30till40_ab, 'old_adult': from40till60_ab, 'old': from60older_ab}		
		self.agent_ab = {'OSX':OSX_ab, 'Windows':windows_ab, 'Linux': linux_ab, 'mobile': mobile_ab}	
		
		self.lan_ab = {'EN': eng_ab, 'NL': nl_ab, 'GE': ger_ab}
				
		self.referer_ab = {'Google':google_ab, 'Bing': bing_ab, 'NA': na_ab}
		
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
		
		age_class = self.get_age_class(context['Age'])

		age_pages = self.age_ab[age_class]
		
		language = str(context['Language'])
		if language == 'NA':
			language = 'EN'
		
		language_pages = self.lan_ab[language]
		
		referer = str(context['Referer'])
		referer_pages = self.referer_ab[referer]
		
		
		#get productids
		product_alpha = (agent_pages[0][0]+age_pages[0][0]+language_pages[0][0]+referer_pages[0][0])/4.0
		product_beta = (agent_pages[0][1]+age_pages[0][1]+language_pages[0][1]+referer_pages[0][1])/4.0
		
		#get_price
		prod_price_alpha = (agent_pages[1][0]+age_pages[1][0]+language_pages[1][0]+referer_pages[1][0])/4.0
		prod_price_beta = (agent_pages[1][1]+age_pages[1][1]+language_pages[1][1]+referer_pages[1][1])/4.0
				
		#get header
		header_alpha = (agent_pages[2][0]+age_pages[2][0]+language_pages[2][0]+referer_pages[2][0])/4.0
		header_beta = (agent_pages[2][1]+age_pages[2][1]+language_pages[2][1]+referer_pages[2][1])/4.0
		
		#get adtype
		adtype_alpha = (agent_pages[3][0]+age_pages[3][0]+language_pages[3][0]+referer_pages[3][0])/4.0
		adtype_beta = (agent_pages[3][1]+age_pages[3][1]+language_pages[3][1]+referer_pages[3][1])/4.0
		
		#get color
		color_alpha = (agent_pages[4][0]+age_pages[4][0]+language_pages[4][0]+referer_pages[4][0])/4.0
		color_beta = (agent_pages[4][1]+age_pages[4][1]+language_pages[4][1]+referer_pages[4][1])/4.0
		
		return product_alpha, product_beta, prod_price_alpha, prod_price_beta, header_alpha, header_beta, adtype_alpha, adtype_beta, color_alpha, color_beta
		
	def get_age_class(self, age):
		if age < 20:
			return 'young'
		elif age < 30:
			return 'young_adult'
		elif age < 40:
			return 'adult'
		elif age < 60:
			return 'old_adult'
		else:
			return 'old'
	
	def update_alpha_betas(self, succes, indexes, context):

		agent = context['Agent']
		age_class = self.get_age_class(context['Age'])
		language = str(context['Language'])
		if language == 'NA':
			language = 'EN'
		referer = str(context['Referer'])
		
		if succes:
			#agent
			self.agent_ab[agent][0][0][indexes[0]] += 1#product
			self.agent_ab[agent][1][0][indexes[1]] += 1#price
			self.agent_ab[agent][2][0][indexes[2]] += 1#header
			self.agent_ab[agent][3][0][indexes[3]] += 1#adtype
			self.agent_ab[agent][4][0][indexes[4]] += 1#color
			
			#age
			self.age_ab[age_class][0][0][indexes[0]] += 1#product
			self.age_ab[age_class][1][0][indexes[1]] += 1#price
			self.age_ab[age_class][2][0][indexes[2]] += 1#header
			self.age_ab[age_class][3][0][indexes[3]] += 1#adtype
			self.age_ab[age_class][4][0][indexes[4]] += 1#color
			
			#language
			self.lan_ab[language][0][0][indexes[0]] += 1#product
			self.lan_ab[language][1][0][indexes[1]] += 1#price
			self.lan_ab[language][2][0][indexes[2]] += 1#header
			self.lan_ab[language][3][0][indexes[3]] += 1#adtype
			self.lan_ab[language][4][0][indexes[4]] += 1#color			
			
			#referer
			self.referer_ab[referer][0][0][indexes[0]] += 1#product
			self.referer_ab[referer][1][0][indexes[1]] += 1#price
			self.referer_ab[referer][2][0][indexes[2]] += 1#header
			self.referer_ab[referer][3][0][indexes[3]] += 1#adtype
			self.referer_ab[referer][4][0][indexes[4]] += 1#color
			
		else:
			#agent
			self.agent_ab[agent][0][1][indexes[0]] += 1#product
			self.agent_ab[agent][1][1][indexes[1]] += 1#price
			self.agent_ab[agent][2][1][indexes[2]] += 1#header
			self.agent_ab[agent][3][1][indexes[3]] += 1#adtype
			self.agent_ab[agent][4][1][indexes[4]] += 1#color
			
			#age
			self.age_ab[age_class][0][1][indexes[0]] += 1#product
			self.age_ab[age_class][1][1][indexes[1]] += 1#price
			self.age_ab[age_class][2][1][indexes[2]] += 1#header
			self.age_ab[age_class][3][1][indexes[3]] += 1#adtype
			self.age_ab[age_class][4][1][indexes[4]] += 1#color
			
			#language
			self.lan_ab[language][0][1][indexes[0]] += 1#product
			self.lan_ab[language][1][1][indexes[1]] += 1#price
			self.lan_ab[language][2][1][indexes[2]] += 1#header
			self.lan_ab[language][3][1][indexes[3]] += 1#adtype
			self.lan_ab[language][4][1][indexes[4]] += 1#color			
			
			#referer
			self.referer_ab[referer][0][1][indexes[0]] += 1#product
			self.referer_ab[referer][1][1][indexes[1]] += 1#price
			self.referer_ab[referer][2][1][indexes[2]] += 1#header
			self.referer_ab[referer][3][1][indexes[3]] += 1#adtype
			self.referer_ab[referer][4][1][indexes[4]] += 1#color
			
			
		
	def save_ab(self, file_path = '../data/alpha_beta/'):
		
		pickle.dump(self.agent_ab, open(file_path + "agent_ab" + str(self.modelid) + ".p", 'wb'))
		pickle.dump(self.age_ab, open(file_path + "age_ab" + str(self.modelid) + ".p", 'wb'))
		pickle.dump(self.lan_ab, open(file_path + "language_ab" + str(self.modelid) + ".p", 'wb'))
		pickle.dump(self.referer_ab, open(file_path + "referer_ab" + str(self.modelid) + ".p", 'wb'))
		
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
	
	def load_ab(self, filepath = '../data/alpha_beta/'):
		
		self.age_ab = pickle.load(open(filepath + 'age_ab'+ str(self.modelid) + '.p','rb'))			
		self.agent = pickle.load(open(filepath + 'agent_ab'+ str(self.modelid) + '.p','rb'))		
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
	
	def run(self, iterations = 80000):
		
		
		for i in range(0, iterations):

			randi = random.randint(0,9900)
			randrunid = random.randint(0,10000)
			context = self.contextGetter.call(randi, randrunid)
			page, pageindex = self.give_page(context)# welke arm wint
			response = responder.respond_with_page(i=randi, runid=randrunid, page = page, teampw = self.teampw)
			
			success = response['effect']['Success'] # 1 of 0
			
			self.update_alpha_betas(success, pageindex, context)

			self.revenue += success*page['price']
			
			if i%1000 == 0:
				self.save_ab()
#				util.save_profit(self.revenue)
			
			util.update_progress(i/iterations)
			
		util.update_progress(1)		
					
def inspect_models(filepath = '../data/alpha_beta/'):
	
	summed_agent = pickle.load(open(filepath + 'agent_ab'+ str(0) + '.p','rb'))	
	summed_age = pickle.load(open(filepath + 'age_ab'+ str(0) + '.p','rb'))		
	
	for i in np.arange(1,10,1):
		temp_agent = pickle.load(open(filepath + 'agent_ab'+ str(i) + '.p','rb'))	
		temp_age =  pickle.load(open(filepath + 'age_ab'+ str(i) + '.p','rb'))
		for key in temp_agent:
			summed_agent[key] = np.add(temp_agent[key], summed_agent[key])
		for key in temp_age:
			summed_age[key] = np.add(temp_age[key], summed_age[key])
				
	
	windows_ab = summed_agent['Windows']/10.0
	OSX_ab = summed_agent['OSX']/10.0
	linux_ab = summed_agent['Linux']/10.0
	mobile_ab = summed_agent['mobile']/10.0
	
	save_model_to_csv(windows_ab, 'windows')
	save_model_to_csv(OSX_ab, 'OSX')
	save_model_to_csv(linux_ab, 'linux')
	save_model_to_csv(mobile_ab, 'mobile')
	
	young_ab = summed_age['young']/10.0
	young_adult_ab= summed_age['young_adult']/10.0
	adult_ab = summed_age['adult']/10.0
	old_adult_ab = summed_age['old_adult']/10
	old_ab = summed_age['old']/10
	
	save_model_to_csv(young_ab, 'young')
	save_model_to_csv(young_adult_ab, 'young_adult')
	save_model_to_csv(adult_ab, 'adult')
	save_model_to_csv(old_adult_ab, 'old_adult')
	save_model_to_csv(old_ab, 'old')
	
	print "done loading"

def save_model_to_csv(model, key, file_path = '../data/model_ab/ '):
	file_name = file_path + key + '.csv'
		
	
	to_save = []
	to_save.append((model[0][0]/model[0][1]).tolist())#product
	to_save.append((model[1][0]/model[1][1]).tolist())#price_product
	to_save.append((model[2][0]/model[2][1]).tolist())#header
	to_save.append((model[3][0]/model[3][1]).tolist())#adtype
	to_save.append((model[4][0]/model[4][1]).tolist())#colors
	with open(file_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(to_save)
		f.close()		
		
	

if __name__ == '__main__':
#	inspect_models()
#	for i in range(5):
#		trainer = ContextTrainer(i, first_timer = True)
#		trainer.run()

