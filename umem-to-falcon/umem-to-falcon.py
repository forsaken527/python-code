#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : QiuMeng
# python2

import requests
import time
import hashlib, json, httplib
import urlparse
import urllib
import sys


public_key  = "ucloudzyh@etouch.cn1431675292000176814293"
private_key = "940029a18e45d14b7eddfc084c0b4fa6109c8c6a"
project_id = "org-27536"
base_url    = "https://api.ucloud.cn"


class UCLOUDException(Exception):
    def __str__(self):
        return "Error"


def _verfy_ac(private_key, params):
    items = params.items()
    items.sort()

    params_data = ""
    for key, value in items:
        params_data = params_data + str(key) + str(value)

    params_data = params_data + private_key

    '''use sha1 to encode keys'''
    hash_new = hashlib.sha1()
    hash_new.update(params_data)
    hash_value = hash_new.hexdigest()
    return hash_value


class UConnection(object):
    def __init__(self, base_url):
        self.base_url = base_url
        o = urlparse.urlsplit(base_url)
        if o.scheme == 'https':
            self.conn = httplib.HTTPSConnection(o.netloc)
        else:
            self.conn = httplib.HTTPConnection(o.netloc)

    def __del__(self):
        self.conn.close()

    def get(self, resouse, params):
        resouse += "?" + urllib.urlencode(params)
        print("%s%s" % (self.base_url, resouse))
        self.conn.request("GET", resouse)
        response = json.loads(self.conn.getresponse().read())
        return response


class UcloudApiClient(object):
    # 添加 设置 数据中心和  zone 参数
    def __init__(self, base_url, public_key, private_key):
        self.g_params = {}
        self.g_params['PublicKey'] = public_key
        self.private_key = private_key
        self.conn = UConnection(base_url)

    def get(self, uri, params):
        # print params
        _params = dict(self.g_params, **params)

        if project_id:
            _params["ProjectId"] = project_id

        _params["Signature"] = _verfy_ac(self.private_key, _params)
        return self.conn.get(uri, _params)


PUSHURl = "http://123.59.43.96:1988/v1/push"


def cleaning_umem(UmemInfoList):
    '''
    data clean
    :param UmemInfoList: 
    :return: list
    '''
    UmemCleanDictList = []
    for item in UmemInfoList:
        del item["Uuid"]
        del item["PrivateIp"]
        del item["Remark"]
        del item["Usage"]
        del item["SubType"]
        del item["ResourceId"]
        del item["CreateTime"]
        del item["Tag"]
        UmemCleanDictList.append(item)
    return UmemCleanDictList


def cleaning_uredis(UredisInfoList):
    '''
    data clean
    :param UredisInfoList: 
    :return: list
    '''
    UredisCleanDictList = []
    for item in UredisInfoList:
        del item["Uuid"]
        del item["PrivateIp"]
        del item["Remark"]
        del item["Usage"]
        del item["ResourceId"]
        del item["CreateTime"]
        del item["Tag"]
        UredisCleanDictList.append(item)
    return UredisCleanDictList


def get_umem_b():
    '''
    umme-bjb
    :return:
    '''
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
            "Action":"GetMetricOverview",
            "Region":"cn-bj2",
            "Zone":"cn-bj2-02",
            "ResourceType":"umem",
            "Limit":50
            }
    response = ApiClient.get("/", Parameters )
    UmemInfoList = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    UmemCleanDictList = cleaning_umem(UmemInfoList)
    return UmemCleanDictList


def get_umem_c():
    '''
    umme-bjc
    :return: 
    '''
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
            "Action":"GetMetricOverview",
            "Region":"cn-bj2",
            "Zone":"cn-bj2-03",
            "ResourceType":"umem",
            "Limit":50
            }
    response = ApiClient.get("/", Parameters )
    UmemInfoList = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    UmemCleanDictList = cleaning_umem(UmemInfoList)
    return UmemCleanDictList



def get_uredis_b():
    '''
    uredis-bjb
    :return: 
    '''
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
            "Action":"GetMetricOverview",
            "Region":"cn-bj2",
            "Zone":"cn-bj2-02",
            "ResourceType":"uredis",
            "Limit":50
            }
    response = ApiClient.get("/", Parameters );
    UredisInfoList = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    UredisCleanDictList = cleaning_uredis(UredisInfoList)
    return UredisCleanDictList


def get_uredis_c():
    '''
    uredis-bjc
    '''
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
            "Action":"GetMetricOverview",
            "Region":"cn-bj2",
            "Zone":"cn-bj2-03",
            "ResourceType":"uredis",
            "Limit":50
            }
    response = ApiClient.get("/", Parameters )
    UredisInfoList = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    UredisCleanDictList = cleaning_uredis(UredisInfoList)
    return UredisCleanDictList


def deal_data(item):
    '''
    格式化
    :param item: 
    :return: 
    '''
    tsTime = int(time.time())
    Name = item["Name"]
    del item["Name"]
    PushDataList = []

    for i in item:
        PushData = {}
        PushData["endpoint"] = Name
        PushData["metric"] = i
        PushData["value"] = item[i]
        PushData["time"] = tsTime
        PushData["counterType"] = "GAUGE"
        PushData["tags"] = ""
        PushData["step"] = 300
        PushDataList.append(PushData)
    return PushDataList


def post_data(PushData):
    PushDataList = []
    PushDataList.append(PushData)
    req = requests.post(PUSHURl, data=json.dumps(PushDataList))
    print req.text



def diff_post(UmemCleanDictList):
    for item in UmemCleanDictList:
        data = deal_data(item)
        for i in data:
            post_data(i)


if __name__ == '__main__':
    UmemCleanDictList = get_umem_c()
    diff_post(UmemCleanDictList)

    UmemCleanDictList = get_umem_b()
    diff_post(UmemCleanDictList)

    UmemCleanDictList = get_uredis_b()
    diff_post(UmemCleanDictList)

    UmemCleanDictList = get_uredis_c()
    diff_post(UmemCleanDictList)
