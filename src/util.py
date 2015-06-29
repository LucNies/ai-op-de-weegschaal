# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 14:56:14 2015

@author: Luc
"""

import sys
import os



# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
# From http://stackoverflow.com/questions/3160699/python-progress-bar
def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
				
				
def save_profit(revenue, file_path = '../data/revenue/'):
	
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	
	filename = file_path + 'revenues_context.txt'
	if not os.path.exists(filename):
		f = open(filename, 'w')
	else:
		f = open(filename, 'a')
		
	f.write(str(revenue) + '\n')
	f.close()

def load_profit(filename =  '../data/revenue/revenues_context.txt'):
	
	f = open(filename, 'r')
	lines = f.readlines();
	
	return int(lines[len(lines)-1])

