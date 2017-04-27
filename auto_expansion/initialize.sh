#!/bin/bash


cd ~

rsync -avz /home/data/* /data/

#copy war host
rsync -avz 10.10.199.5::data/tmp/peacock/peacock.war /data/etouch/8080_tomcat_server/webapps/
rsync -avz 10.10.199.5::data/tmp/peacock/peacock.war /data/etouch/8081_tomcat_server/webapps/
rsync -avz 10.10.199.5::data/tmp/peacock/hosts /etc/hosts

