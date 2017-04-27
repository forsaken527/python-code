#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Author : QiuMeng


import urllib
import urllib2
import json
import datetime

Retention = 30

today = datetime.datetime.now()

def http_delete(index_name):
    url = 'http://127.0.0.1:9200/' + index_name
    request = urllib2.Request(url)
    request.get_method = lambda:'DELETE'
    request = urllib2.urlopen(request)
    return request.read()

home_url = 'http://127.0.0.1:9200/_cat/indices'
response = urllib2.urlopen(home_url)
index_list = response.read()

file = open('Index_List','w+')
file.write(index_list)

file = open('Index_List','r')
for line in file.readlines():
    for i in line.split('\t'):
        index_date = i.split()[2][-10:]
        if len(index_date) == 10:
            date_day = datetime.datetime.strptime(index_date,'%Y.%m.%d')
            diff = (today-date_day).days
            if diff > Retention:
                index_name = i.split()[2]
                http_delete(index_name)

file.close()
