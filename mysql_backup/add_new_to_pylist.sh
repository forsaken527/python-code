#!/bin/bash

# help menu
usage()
{
        echo 
        echo "usage: sh $0 "mysql_shard_name"
        echo 
        exit
}

# check the number of parameter
if [[ $# != 2 ]];then
        usage
fi

sed -i '/"mysql.shard.2047.m.zhwnl.freed.so",/a\    "'$1'",' mysql_shard_crontab.py
