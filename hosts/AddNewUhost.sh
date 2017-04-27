#!/bin/bash
usage()
{
        echo 
        echo "usage: sh $0 ipaddress hostname"
        echo 
        exit
}

# check the number of parameter
if [[ $# != 2 ]];then
        usage
fi

ipaddress=$1
hostname=$2

#add/etc/hosts

sed -i "/\#others/a\\$ipaddress    $hostname"  etc/hosts

#add/rundeck

des=`echo $hostname | awk -F. '{print $2}'`
xml="<node name=\"$hostname\" description=\"$des\" tags=\"$des\" hostname=\"$hostname\" osArch=\"amd64\" osFamily=\"unix\" osName=\"Linux\" osVersion=\"2.6.32-431.11.9.el6.ucloud.x86_64\" username=\"root\"/>"
sed -i "/Udoor/a\  $xml" rundeck/resources.xml

#add/ansible

sed -i "/\[all\_nodes\]/a\\$hostname"  ansible/hosts
