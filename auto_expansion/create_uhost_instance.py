#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json

'''
使用前请再次修改uhost的相关配置，相关配置的范围请参考官方api文档
https://docs.ucloud.cn/api/uhost-api/create_uhost_instance
'''

region="cn-bj2"
zone="cn-bj2-02"
imageid="uimage-1jccs1"  #m-api1.zhwnl.freed.so
password="c3N5I3VjbG91ZDIwMTY="   #base64
cpu=4
memory=16384  #16G
disk_type="LocalDisk"
disk_space=10
boot_disk_space=20
tag="ops"
firewalld_id=33111

Parameters = {
    "Action": "CreateUHostInstance",
    "Region": region,
    "Zone": zone,
    "ImageId": imageid,
    "LoginMode": "Password",
    "Password": password,
    "CPU": cpu,
    "Memory": memory,
    "StorageType":disk_type,
    "DiskSpace": disk_space,
    "BootDiskSpace": boot_disk_space,
    "ChargeType": "Dynamic",
    "Tag": tag,
    "UHostType": "Normal",
    "SecurityGroupId": firewalld_id,
    "Name": "peacock_flexible_host"
}

if __name__=='__main__':
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    response = ApiClient.get("/", Parameters);
    callback=json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
    back_dict=json.loads(callback)
    print back_dict["IPs"][0],back_dict["UHostIds"][0]
