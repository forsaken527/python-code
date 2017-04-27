#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Author : QiuMeng


import urllib2
import hashlib, json, httplib
import urlparse
import urllib
import sys
import redis



uredis_name_list = []
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



if len(sys.argv) == 1:
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    # describe
    Parameters = {"Action": "DescribeUMemSpace", "Region": "cn-bj2", "Limit": 110}
    response = ApiClient.get("/", Parameters)
    dis_umem_list = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    for item in dis_umem_list:
        uredis_name_list.append(item["Name"])

    # master-slave
    Parameters = {
        "Action": "DescribeURedisGroup", "Limit": 110, "Offset": 0, "Region": "cn-bj2"
    }
    response = ApiClient.get("/", Parameters);
    json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
    ms_umem_list = json.loads(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))["DataSet"]
    for item in ms_umem_list:
        uredis_name_list.append(item["Name"])
    #print uredis_name_list,len(uredis_name_list)
    for uredis_name in uredis_name_list:
        update_times = redis_server.get(uredis_name)
        if update_times == "3":
            redis_server.set(uredis_name,0)

if len(sys.argv) == 2:
    update_uredis_name = sys.argv[1]
    redis_server.set(update_uredis_name, 0)



