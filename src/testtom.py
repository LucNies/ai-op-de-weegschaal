# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:30 2015

@author: Tom
"""

import requests
import numpy as np
import json
from pprint import pprint


response_url = 'http://krabspin.uci.ru.nl/proposePage.json/'
content_url = 'http://krabspin.uci.ru.nl/getcontext.json/'

team_id = 'PyBandits'
team_pass = 'e6e2343579d1d394a9be2d6cc0de9ee0'

run_id = 0


contextarray = []
responsearray = []



contextdir = 'contextrunid00000.json'
responsedir = 'responserunid00000.json'
print "start gathering..."


for i in range(0,100):
    context_payload = {'i': i, 'runid' : run_id, 'teamid' : team_id, 'teampw' : team_pass }   
    
    context = requests.get(content_url, params = context_payload).json()
    contextarray.append(context)

    propose_payload = {'i': i, 'runid': run_id, 'teamid': team_id, 'header': 15, 'adtype': 'square', 'color': 'green', 'productid':11, 'price': 40.0, 'teampw': team_pass}
    response  = requests.get(response_url, params = propose_payload).json()
    responsearray.append(context)

    
with open(contextdir, 'w+') as contextfile:
    json.dump(contextarray, contextfile)
with open(responsedir, 'w+') as responsefile:
    json.dump(responsearray, responsefile)
print 'written contexts to ' + contextdir + ' and responses to ' + responsedir + '.'


with open(contextdir) as contextfile:
    contextdata = json.load(contextfile)
pprint(contextdata)

















