#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : QiuMeng

import requests
import json
import configparser
import re

config = configparser.ConfigParser()
HomeUrl = "http://devops.etouch.cn/api/jasset/host/?hostname="


def analyse():
    '''
    根据api获取相关信息，按照分组进行处理
    :return:返回一个以分组为key，ip和hostname为value的字典(dic)
    '''
    result = requests.get(HomeUrl)
    result = json.loads(result.text)
    with open('example.ini', 'w') as test:
        pass# 初始化
    for item in result:
        if "all" in item["group"]:
            AllIndex = item["group"].index("all")
            del item["group"][AllIndex]
        if len(item["group"]) == 2:
            config[item["group"][0]] = {
                item["ip"]:item["hostname"]
            }
            with open('example.ini', 'a') as configfile:
                config.write(configfile)
            config[item["group"][1]] = {
                item["ip"]: item["hostname"]
            }
            with open('example.ini', 'a') as configfile:
                config.write(configfile)
        elif len(item["group"]) == 1:
            config[item["group"][0]] = {
                item["ip"]: item["hostname"]
            }
            with open('example.ini', 'a') as configfile:
                config.write(configfile)

    #按照分组，获取新的结果
    HostProject = {}
    with open("example.ini",'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('['):
                project = re.sub("[\[]|[\]]", "", line)  # project = peacock
                HostProject[project] = {}
    with open("example.ini", 'r', encoding='utf-8') as f:
        flag = False
        project = None
        for line in f:
            line = line.strip()
            if line.startswith('['):
                flag = True
                project = re.sub("[\[]|[\]]", "", line)
                continue
            if flag:
                LineList = line.split('=')
                Ipaddress = re.sub(" ",'',LineList[0])
                Hostname = re.sub(" ",'',LineList[1])
                HostProject[project][Ipaddress] = Hostname
                flag = False
    if "all" in HostProject.keys():
        del HostProject["all"]
    return HostProject



def update_host(HostProject):
    with open("hosts","w",encoding="utf-8") as f:
        for item in HostProject:
            block = HostProject[item]
            ProjectName = '['+item+']'
            f.write(ProjectName+'\n')
            for i in HostProject[item]:
                Ipaddress = i
                hostname = HostProject[item][i]
                line = Ipaddress + '\t' + hostname
                f.write(line+'\n')


if __name__ == '__main__':
    update_host(analyse())