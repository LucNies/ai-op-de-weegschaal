# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:30 2015

@author: Luc
"""


import context_getter
import responder


if __name__ == '__main__':
    runid = 10
    for i, context in enumerate(context_getter.ContextGetter(runid, max_calls = 10)):
        print "context: "
        print context
        
        response = responder.respond(i, runid)
        print "response: "
        print response