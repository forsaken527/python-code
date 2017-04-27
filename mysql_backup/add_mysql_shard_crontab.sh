#!/bin/bash

#python mysql_shard_crontab.py > mysql_shard_list

cat mysql_shard_list | while read line
do 
host=`echo $line | awk '{print $4}'`
min=`echo $line | awk '{print $1}'`
hour=`echo $line | awk '{print $2}'`
week=`echo $line | awk '{print $3}'`
ssh -i ~/.ssh/id_rsa_root  root@$host "echo ''$min' '$hour' '*' '*' '$week' sh /data/mysql_backup/full_backup.sh' >> /var/spool/cron/root"	
ssh -i ~/.ssh/id_rsa_root  root@$host "echo ''1' '1' '*' '*' '*' sh /data/mysql_backup/incre_backup.sh' >> /var/spool/cron/root"	
ssh -i ~/.ssh/id_rsa_root  root@$host "yum install nfs-utils -y"
ssh -i ~/.ssh/id_rsa_root  root@$host "rsync -avz 10.10.199.5::data/tmp/mysql_backup /data/"
ssh -i ~/.ssh/id_rsa_root  root@$host "sed -i 's/hostname\=\`hostname\`/hostname\=$host/g' /data/mysql_backup/full_backup.sh"
ssh -i ~/.ssh/id_rsa_root  root@$host "sed -i 's/hostname\=\`hostname\`/hostname\=$host/g' /data/mysql_backup/incre_backup.sh"
ssh -i ~/.ssh/id_rsa_root  root@$host "mkdir -p /data/mnt/"
ssh -i ~/.ssh/id_rsa_root  root@$host "mount -t nfs 10.9.108.228:/UDisk/log_backup_for_mysql /data/mnt"
ssh -i ~/.ssh/id_rsa_root  root@$host "mkdir -p /data/mnt/$host"

done
