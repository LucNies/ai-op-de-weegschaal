# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:30 2015

@author: Luc
"""

import requests


content_url = 'http://krabspin.uci.ru.nl/getcontext.json/'
team_id = 'PyBandits'
team_pass = 'e6e2343579d1d394a9be2d6cc0de9ee0'
i = 1
run_id = 10

context_payload = {'i': i, 'runid' : run_id, 'teamid' : team_id, 'teampw' : team_pass }


response_url = 'http://krabspin.uci.ru.nl/proposePage.json/'
propose_payload = {'i': i, 'runid': run_id, 'teamid': team_id, 'header': 15, 'adtype': 'square', 'color': 'green', 'productid':11, 'price': 40.0, 'teampw': team_pass}


print "getting request"
context = requests.get(content_url, params = context_payload).json()
response  = requests.get(response_url, params = propose_payload).json()
print "done"
