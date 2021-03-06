# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:57:58 2015

@author: Luc
"""
import numpy as np
import requests
import json

headers = [5, 15, 35]
adtypes = ['skyscraper', 'square', 'banner']
colors = ['green', 'blue', 'red', 'black', 'white']
productid = np.arange(10, 26, 1)
prices = np.arange(0, 50.01, 0.01)


def respond(i, runid, teampw, teamid = 'PyBandits', url = 'http://krabspin.uci.ru.nl/proposePage.json/'):
    page = {'i': i, 'runid': runid, 'teamid': teamid, 'header': headers[0], 'adtype': adtypes[0], 'color': colors[0], 'productid': productid[10], 'price': prices[10], 'teampw': teampw}
    response = requests.get(url, params = page).json()
    return response


def respond_with_page(i, runid, page, teampw, teamid = 'PyBandits', url = 'http://krabspin.uci.ru.nl/proposePage.json/'):
    page['teamid']= teamid
    page['teampw']= teampw
    page['i']=i
    page['runid']=runid
    
    response = requests.get(url, params = page).json()
    return response



if __name__ == '__main__':
    bla = respond(1, 10)
    print bla['effect']['Success']
    