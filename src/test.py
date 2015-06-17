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

if __name__ == '__main__':
    a, b = 1 , 1
    lijst  = beta.rvs(a,b, size = 1000)
    print lijst
    plt.hist(lijst)
    
    