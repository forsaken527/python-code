#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Author : QiuMeng
############
#############
import sys
import os

mysql_shard_list = [
    "mysql.shard.2000.m.zhwnl.freed.so",
    "mysql.shard.2001.m.zhwnl.freed.so",
    "mysql.shard.2002.m.zhwnl.freed.so",
    "mysql.shard.2003.m.zhwnl.freed.so",
    "mysql.shard.2004.m.zhwnl.freed.so",
    "mysql.shard.2005.m.zhwnl.freed.so",
    "mysql.shard.2006.m.zhwnl.freed.so",
    "mysql.shard.2007.m.zhwnl.freed.so",
    "mysql.shard.2008.m.zhwnl.freed.so",
    "mysql.shard.2009.m.zhwnl.freed.so",
    "mysql.shard.2010.m.zhwnl.freed.so",
    "mysql.shard.2011.m.zhwnl.freed.so",
    "mysql.shard.2012.m.zhwnl.freed.so",
    "mysql.shard.2013.m.zhwnl.freed.so",
    "mysql.shard.2014.m.zhwnl.freed.so",
    "mysql.shard.2015.m.zhwnl.freed.so",
    "mysql.shard.2016.m.zhwnl.freed.so",
    "mysql.shard.2017.m.zhwnl.freed.so",
    "mysql.shard.2018.m.zhwnl.freed.so",
    "mysql.shard.2019.m.zhwnl.freed.so",
    "mysql.shard.2020.m.zhwnl.freed.so",
    "mysql.shard.2021.m.zhwnl.freed.so",
    "mysql.shard.2022.m.zhwnl.freed.so",
    "mysql.shard.2023.m.zhwnl.freed.so",
    "mysql.shard.2024.m.zhwnl.freed.so",
    "mysql.shard.2025.m.zhwnl.freed.so",
    "mysql.shard.2026.m.zhwnl.freed.so",
    "mysql.shard.2027.m.zhwnl.freed.so",
    "mysql.shard.2028.m.zhwnl.freed.so",
    "mysql.shard.2029.m.zhwnl.freed.so",
    "mysql.shard.2030.m.zhwnl.freed.so",
    "mysql.shard.2031.m.zhwnl.freed.so",
    "mysql.shard.2032.m.zhwnl.freed.so",
    "mysql.shard.2033.m.zhwnl.freed.so",
    "mysql.shard.2034.m.zhwnl.freed.so",
    "mysql.shard.2035.m.zhwnl.freed.so",
    "mysql.shard.2036.m.zhwnl.freed.so",
    "mysql.shard.2037.m.zhwnl.freed.so",
    "mysql.shard.2038.m.zhwnl.freed.so",
    "mysql.shard.2039.m.zhwnl.freed.so",
    "mysql.shard.2040.m.zhwnl.freed.so",
    "mysql.shard.2041.m.zhwnl.freed.so",
    "mysql.shard.2042.m.zhwnl.freed.so",
    "mysql.shard.2043.m.zhwnl.freed.so",
    "mysql.shard.2044.m.zhwnl.freed.so",
    "mysql.shard.2045.m.zhwnl.freed.so",
    "mysql.shard.2046.m.zhwnl.freed.so",
    "mysql.shard.2047.m.zhwnl.freed.so",
]
time_dic = {
    0:"01:01",
    1:"01:31",
    2:"02:01",
    3:"02:31",
    4:"03:01",
    5:"03:31",
    6:"04:01",
    7:"04:31",
    8:"05:01",
    9:"05:31",
    10:"06:01",
    11:"06:31",
    12:"07:01",
    13:"07:31",
    14:"08:01",
    15:"08:31",
    16:"09:01",
}

def create_cron_all():
    for line in mysql_shard_list:
        shard_num = int(line[13:16])
        week_num = shard_num % 7
        day_num = shard_num // 7
        cron_hour = int(time_dic[day_num][0:2])
        cron_min = int(time_dic[day_num][3:])
        print cron_min,cron_hour,week_num,line 

def add_new_shard(shard_name):
    mysql_shard_list.append(shard_name)
    shard_num = int(shard_name[13:16])
    week_num = shard_num % 7
    day_num = shard_num // 7
    cron_hour = int(time_dic[day_num][0:2])
    cron_min = int(time_dic[day_num][3:])
    print cron_min, cron_hour,week_num, shard_name 

#user_input = raw_input("add new mysql shard:[a];create all crontab:[c]:")
#if user_input == 'a':
#    shard_name = raw_input("shard_name:")
#    add_new_shard(shard_name)
#if user_input == 'c':
#create_cron_all()
if len(sys.argv) == 1:
    create_cron_all()
else:
    add_new_shard(sys.argv[1])
    #user_input = raw_input("add new mysql shard name:")
    #add_new_shard(user_input)
    
