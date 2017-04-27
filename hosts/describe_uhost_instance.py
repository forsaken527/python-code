#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib, json, httplib
import urlparse
import urllib
import sys


public_key  = ""
private_key = ""
project_id = ""
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

if __name__=='__main__':
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters = {
                "Action":"DescribeUHostInstance",
                "Region":"cn-bj2",
                "Limit":500,
               }
    response = ApiClient.get("/", Parameters);
    UrlList=json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
    UhostInfoList=json.loads(UrlList)
    uhost_list=UhostInfoList["UHostSet"]
    files = open("Hosts_List",'w+')
    for i in uhost_list:
        Network = i["IPSet"][0]["IP"]
        Hostname = i["Name"]
        files.write(Network)
        files.write('\t')
        files.write(Hostname)
        files.write('\n')
    files.close()
