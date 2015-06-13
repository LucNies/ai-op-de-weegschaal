# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 13:52:29 2015

@author: Luc
"""

from __future__ import division
import context_getter
import os 
import json
import util

def store(runid, file_path = '../context/', i = 0):
    if not os.path.exists(file_path):
            os.makedirs(file_path)
            
    contextarray = []
    getter = context_getter.ContextGetter(runid)

    print 'getting context of run: ' + str(runid)
    util.update_progress(0)
    for i, context in enumerate(getter):
        contextarray.append(context)        
        util.update_progress(i/getter.max_calls)
    util.update_progress(1)
      
    print 'writing context to json'      
    with open(file_path + str(runid), 'w+') as contextfile:
        json.dump(contextarray, contextfile)

if __name__ == '__main__':
    
    #for i in range(75,300):
     #   print "Bezig met runid: " + str(i)
    store(300)

    