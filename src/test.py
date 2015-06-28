# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:30 2015

@author: Luc
"""


import context_getter
import responder
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from json import JSONDecoder


if __name__ == '__main__':
	path = "../context/"
	file_names = os.listdir(path)	

	

	f = open(path+file_names[0], 'r')
	content = json.load(f)
	print "loaded"

	