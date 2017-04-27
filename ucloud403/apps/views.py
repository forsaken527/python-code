#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Author : QiuMeng
#python version=2.7.12
#django version=1.10.5
#py_redis_connecter version=2.10.5


from django.shortcuts import render,render_to_response
from django.shortcuts import HttpResponse
import random
import urllib2
import urllib
import os
import datetime
import redis


#redis_config
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
VERIFICATION_CODE_TIMEOUT = 60

#redis_connection_pool
redis_pool = redis.ConnectionPool(host=REDIS_HOST,port=REDIS_PORT)
redis_server = redis.Redis(connection_pool=redis_pool)



def index(request):
    now = datetime.datetime.now()
    return render(request,"index.html")

def update_deny_config(address):
    os.system("rsync -az /usr/local/tengine/conf/deny.conf /tmp/")
    conf = open("/tmp/deny.conf","a")
    line = "allow" '\t' + address + ';' + '\n'
    conf.write(line)
    conf.close()
    os.system("rsync -az /tmp/deny.conf /usr/local/tengine/conf/")
    os.system("/etc/init.d/tengine reload")


def code(*args,**kwargs):
    li = []
    for i in range(6):
        r = random.randrange(0, 5)
        if r == 2 or r == 4:
            num = random.randrange(0, 10)
            li.append(str(num))
        else:
            i = random.randrange(97, 123)
            li.append(chr(i))

    result = "".join(li)
    return result



def sender(phone_number,auth_code):
    sms_http_url = "http://alarm.etouch.cn/dbj/api/ops/sms_notifys"
    post_values = {
        "tos":phone_number,
        "subject":"SMS_code",
        "content":"Your Verification Code is:" + '>>>' + (auth_code) + '<<<',
    }
    post_data = urllib.urlencode(post_values)
    # print post_data
    request = urllib2.Request(sms_http_url,post_data)
    response = urllib2.urlopen(request)


def Verification_password(request):

    if request.GET["auth_code"]:
        phone_number = request.GET['phone_number']
        input_code = request.GET['auth_code']
        if input_code:
            local_password = redis_server.get(phone_number)
            if local_password:
                if local_password == input_code:
                    message = "Welcome"
                else:
                    message = "Reject"
            else:
                message = "Overdue"
        else:
            message = 'Input_Empty'
    else:
        message = "GET_Empty"

    return HttpResponse(message)


def login(request):
    if request.GET['phone_number']:
        input_code = request.GET['phone_number']
        if input_code.isdigit() and len(input_code) == 11:
            phone_number = request.GET['phone_number']
            f = open('db', 'r')
            for line in f:
                line_list = line.strip().split("|")
                if line_list[0] == phone_number:
                    new_code = code()
                    redis_server.set(phone_number,new_code,ex=VERIFICATION_CODE_TIMEOUT)
                    sender(phone_number,new_code)
                    message_a = 'You searched for: %s' % line_list[1]
                    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                        address = request.META['HTTP_X_FORWARDED_FOR']
                    else:
                        address = request.META['REMOTE_ADDR']
                    update_deny_config(address)
                    return render_to_response("Verification.html", {"current_message": message_a,
                                                                    "current_phone": phone_number,
                                                                    "current_timeout": VERIFICATION_CODE_TIMEOUT,
                                                                    "address":address,
                                                                    })
                else:
                    message = "You are not register!"
            f.close()
        else:
            message = "Illegal input"
    else:
        message = 'You submitted an empty form.'
    return render_to_response("access.html",{"current_message":message})