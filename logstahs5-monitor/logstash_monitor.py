#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : QiuMeng

import requests
import time
import datetime
import logging
import json


HOSTNAME = "node1.flume.log.freed.so"
HOMEURL = "http://127.0.0.1/9600/_node/stats/pipeline"
PUSHURl = "http://127.0.0.1:1988/v1/push"

days = time.strftime("%Y-%m-%d",time.gmtime())

LOG_NAME_LIST = [
    "/data/etouch/nginx/log/log-dmp.suishenyun.cn.access.log-%s"%days,
    "/data/etouch/nginx/log/log-dmp.suishenyun.cn.access.log-collect_ce_log-%s"%days,
    "/data/etouch/nginx/log/pcstats.suishenyun.net.access.log-%s"%days
]

def get_data():
    '''
    从logstash的api中获取数据
    :return: dict
    '''
    # TODO 修改地址
    data = requests.get("http://123.59.128.11/_node/stats/pipeline")
    DataDic = json.loads(data.text)
    del DataDic["id"]  # 删除一些不需要的数据
    del DataDic["version"]
    del DataDic["http_address"]
    del DataDic["name"]
    return DataDic


def deal_data():
    '''
    将获取的数据进行整理处理格式化，
    :return: 
    '''
    tsTime = int(time.time())
    DataDic =  get_data()
    PushData = {}
    for item in ["in","out","filtered"]:
        PushData[item] = {}
        PushData[item]["endpoint"] =  HOSTNAME
        PushData[item]["metric"] = "logstash-collect-%s-amount"%item
        PushData[item]["value"] = DataDic["pipeline"]["events"][item]
        PushData[item]["time"] = tsTime
        PushData[item]["counterType"] = "GAUGE"
        PushData[item]["tags"] = ""
        PushData[item]["step"] = 300
    return PushData


def post_data():
    '''
    基本数据格式
    {
		'endpoint': 'node1.flume.log.freed.so', 
		'metric': 'logstash-collect-in-amount', 
		'value': 213,
		'time': 1490691250, 
		'counterType': 'GAUGE',
		'tags': '', 
		'step': 300
	} 
    将处理过后的数据进行推送到open-falcon的push接口
    :return: 
    '''
    PushData = deal_data()
    for item in PushData:
        response = requests.post(PUSHURl,data=json.dumps(PushData[item]))


def get_log_amount():
    '''
    统计日志列表中的文件数量
    :return: 返回各个日志文件的数量(dict)
    '''
    logs_amount = {}
    for item in LOG_NAME_LIST:
        count = 0
        with open(item,"r") as f:
            for line in f:
                count += 1
                pass
        logs_amount[item] = count

    return logs_amount


if __name__ == '__main__':
    post_data()