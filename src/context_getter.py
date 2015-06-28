# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:18:13 2015

@author: Luc
"""

import requests


class ContextGetter(object):
    
    
    def __init__(self, runid, url = 'http://krabspin.uci.ru.nl/getcontext.json/', teamid = 'PyBandits', pass_file = '../password.pass', start = 0, max_calls = 10000):
        f = open(pass_file, 'rb')
        teampw = f.next()
        self.url = url
        self.i = start
        self.max_calls = max_calls
        self.arguments = {'i': self.i, 'runid' : runid, 'teamid' : teamid, 'teampw' : teampw }
    
    def __iter__(self):
        return self
    
    def next(self):
        if(self.i > self.max_calls):
            raise StopIteration
        
        else:
            context = self.call(self.i)
            self.i+=1
            
            return context
        
    
    def call(self, i, runid):
        self.arguments['i'] = i
	self.arguments['runid'] = runid
        context = requests.get(self.url, params = self.arguments).json()
        return context['context']

if __name__ == '__main__':
    runid = 1000
    
    users = ContextGetter(runid = runid)
    
    for i, context in enumerate(users):
        if i>10:
            break
        else:
            print context