#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Author : QiuMeng


from sdk import UcloudApiClient
from config import *
import sys
import json

uhost_id = sys.argv[1]

if __name__=='__main__':
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters = {
        "Action":"TerminateUHostInstance",
        "Region":"cn-bj2",
        "Zone":"cn-bj2-02",
        "UHostId":uhost_id
    }
    response = ApiClient.get("/", Parameters);
    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
