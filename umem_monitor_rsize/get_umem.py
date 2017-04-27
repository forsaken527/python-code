#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : QiuMeng
#version 0.1.1



import redis
import urllib2
import hashlib, json, httplib
import urlparse
import urllib
import sys


PHONE_NUMBER = 15810909368
Distributed_umem_dic = {}
Master_slaveUMemSpace_dic = {}

#redis_config
REDIS_HOST = "10.10.6.137"
REDIS_PORT = 6379
VERIFICATION_CODE_TIMEOUT = 60
#redis_connection_pool
redis_pool = redis.ConnectionPool(host=REDIS_HOST,port=REDIS_PORT)
redis_server = redis.Redis(connection_pool=redis_pool)


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


def sender():
    sms_http_url = "http://alarm.etouch.cn/dbj/api/ops/sms_notifys"
    post_values = {
        "tos":PHONE_NUMBER,
        "subject":"SMS_code",
        "content":"mem used exseed %99 and auto expansion 3 times",
    }
    post_data = urllib.urlencode(post_values)
    request = urllib2.Request(sms_http_url,post_data)
    response = urllib2.urlopen(request)


def ResizeUMemSpace(umem_id,size):
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
                "Action":"ResizeUMemSpace",
                "Region":"cn-bj2",
                "SpaceId":umem_id,
                "Size":size,
               }
    response = ApiClient.get("/", Parameters);
    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))



def ResizeRedisSpace(redis_id,size):
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters={
                "Action":"ResizeURedisGroup",
                "Region":"cn-bj2",
                "GroupId":redis_id,
                "Size":size,
               }
    response = ApiClient.get("/", Parameters);
    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))


#=======================================================================================================================
##main
#=======================================================================================================================


if __name__=='__main__':
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
#describe
    Parameters = {"Action": "DescribeUMemSpace", "Region": "cn-bj2", "Limit": 110}
    response = ApiClient.get("/", Parameters)
    dis_umem_list = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    for item in dis_umem_list:
        Distributed_umem_dic["umem_name"] = item["Name"]
        Distributed_umem_dic["umem_use"] = item["UsedSize"]
        Distributed_umem_dic["umem_size"] = item["Size"]*1024.000
        Distributed_umem_dic["umem_id"] = item["SpaceId"]
        Distributed_umem_dic["use_percent"] = float("%.2f "%(Distributed_umem_dic["umem_use"]/Distributed_umem_dic["umem_size"]))
        print Distributed_umem_dic
        if Distributed_umem_dic["use_percent"] >= 0.98:
            update_times = redis_server.get(Distributed_umem_dic["umem_name"])
            if update_times == None:
                redis_server.set(Distributed_umem_dic["umem_name"],0)
            else:
                rsize_times = int(update_times)
                if rsize_times < 3:
                    ResizeUMemSpace(Distributed_umem_dic["umem_id"],int((Distributed_umem_dic["umem_size"]/1024)+4))
                    print "########WARNING#############\n"
                    print Distributed_umem_dic["umem_name"],"auto expansion times is :",rsize_times+1,'\n'
                    rsize_times += 1
                    redis_server.set(Distributed_umem_dic["umem_name"],rsize_times)
                else:
                    sender()
                    print "########WARNING#############"
                    print Distributed_umem_dic["umem_name"],"auto expansion times is :",rsize_times,'\n'

#master-slave
    Parameters={
        "Action":"DescribeURedisGroup","Limit":110,"Offset":0,"Region":"cn-bj2"
    }
    response = ApiClient.get("/", Parameters);
    json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
    ms_umem_list = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    for item in ms_umem_list:
        Master_slaveUMemSpace_dic["umem_name"] = item["Name"]
        Master_slaveUMemSpace_dic["umem_use"] = item["UsedSize"]
        Master_slaveUMemSpace_dic["umem_size"] = item["Size"]*1024.000
        Master_slaveUMemSpace_dic["umem_id"] = item["GroupId"]
        Master_slaveUMemSpace_dic["use_percent"] = float("%.2f "%(Master_slaveUMemSpace_dic["umem_use"]/Master_slaveUMemSpace_dic["umem_size"]))
        print Master_slaveUMemSpace_dic
        if Master_slaveUMemSpace_dic["use_percent"] >= 0.98:
            update_times = redis_server.get(Master_slaveUMemSpace_dic["umem_name"])
            if update_times == None:
                redis_server.set(Master_slaveUMemSpace_dic["umem_name"],0)
            else:
                rsize_times = int(update_times)
                if rsize_times < 3:
                    ResizeRedisSpace(Master_slaveUMemSpace_dic["umem_id"],int((Master_slaveUMemSpace_dic["umem_size"]/1024)*2))
                    print "########WARNING#############"
                    print Master_slaveUMemSpace_dic["umem_name"],"auto expansion times is :",rsize_times+1,
                    rsize_times += 1
                    redis_server.set(Master_slaveUMemSpace_dic["umem_name"],rsize_times)
                else:
                    sender()


#=======================================================================================================================
##main_the end!
#=======================================================================================================================
