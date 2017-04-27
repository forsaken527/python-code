#!/bin/bash


while read line
    do
        hostname_line=`echo $line |awk '{print $2}'`
        grep $hostname_line /etc/ansible/hosts
        if [ $? -ne 0 ];then
            sed -i "/\[all\_nodes\]/a\\$hostname_line"  /etc/ansible/hosts
        fi
done < Hosts_List


while read line
    do
        hostname_line=`echo $line |awk '{print $2}'`
        grep $hostname_line /etc/hosts
        if [ $? -ne 0 ];then
           sed -i "/\#others/a\\$line"  /etc/hosts
        fi
done < Hosts_List




while read line
    do
        hostname_line=`echo $line |awk '{print $2}'`
        grep $hostname_line /var/rundeck/projects/all_nodes/etc/resources.xml
        if [ $? -ne 0 ];then
            des=`echo $hostname_line | awk -F. '{print $2}'`
            xml="<node name=\"$hostname_line\" description=\"$des\" tags=\"$des\" hostname=\"$hostname_line\" osArch=\"amd64\" osFamily=\"unix\" osName=\"Linux\" osVersion=\"2.6.32-431.11.9.el6.ucloud.x86_64\" username=\"root\"/>"
            sed -i "/Udoor/a\  $xml" /var/rundeck/projects/all_nodes/etc/resources.xml 
        fi
done < Hosts_List
