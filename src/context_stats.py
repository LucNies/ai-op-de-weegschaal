# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:30 2015

@author: Luc
"""

from __future__ import division
import context_getter
import responder
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from json import JSONDecoder
import util


poss_languages = {'EN': 0, 'NL':1, 'GE':2, 'NA':3}
poss_agents = {'OSX':0, 'Windows':1, 'Linux':2, 'mobile':3}
poss_refers = {'Google':0, 'Bing':1, 'NA':2}
poss_ages = np.arange(10, 112, 1)
poss_ages[len(poss_ages)-1] = 111



class ContextStats(object):
	
	
	def __init__(self):
		self.ages = np.zeros(len(poss_ages))
		self.agents = np.zeros(len(poss_agents))
		self.languages = np.zeros(len(poss_languages))
		self.refers = np.zeros(len(poss_refers))
	
	def save(self, filename = "../data/context_stats"):
		
		
		np.savez(filename,
		ages = self.ages,
		agents = self.agents,
		languages = self.languages,
		refers = self.refers)
	
	def load(self, filename = "../data/context_stats.npz"):
		
		data = np.load(filename)
		
		self.ages = data['ages']
		self.agents = data['agents']
		self.languages = data['languages'] 
		self.refers = data['refers']

		data.close()

	def parse_context(self, context):
		
		age = context['Age']
		agent = str(context['Agent'])
		language = str(context['Language'])
		refer = str(context['Referer'])
		
		if age != 999:
			self.ages[age-10]+=1
		else:
			self.ages[len(self.ages)-1]+=1
		
		self.agents[poss_agents[agent]]+=1
		self.languages[poss_languages[language]]+=1
		self.refers[poss_refers[refer]]+=1
		
	def plot_data(self):
		
		#plot age
		plt.xlabel('age')
		plt.ylabel('frequency')
		plt.bar(poss_ages, self.ages)
		plt.savefig('../data/plots/age_plot.png')

		#plot agent
		
#		plt.xlabel('agent')
#		plt.ylabel('frequency')
#		plt.bar(range(len(poss_agents)), self.agents)
#		plt.savefig('../data/plots/agent_plot.png')		
#		
		# plot languages
		print self.languages
#		plt.xlabel('languages')
#		plt.ylabel('frequency')
#		plt.bar(range(len(poss_languages)), self.languages)
#		plt.savefig('../data/plots/languages_plot.png')
#		
		# plot languages
		print self.refers
#		plt.xlabel('refers')
#		plt.ylabel('frequency')
#		plt.bar(range(len(poss_refers)), self.refers)
#		plt.savefig('../data/plots/refers_plot.png')
		


if __name__ == '__main__':
	path = "../context/"
	file_names = os.listdir(path)	
	
	stats = ContextStats()
	stats.load()
	stats.plot_data()

#	f = open(path+file_names[0], 'r')
#	content = json.load(f)	
#
#	nfiles = len(file_names)	
#	util.update_progress(0)	
#	
#	for i, name in enumerate(file_names):
#		f = open(path+name, 'r')
#		content = json.load(f)		
#		
#		for context in content:
#			stats.parse_context(context)
#		
#		stats.save()
#		util.update_progress(i/nfiles)
		
	


	
	print "loaded"

	