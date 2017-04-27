# mysql_backup.sh
#!/bin/sh
rq=` date +"%Y_%m_%d" `
Ddump=`date -d '-7 days' +"%Y_%m_%d"`
Dbinlog=`date -d '-7 days' +"%Y-%m-%d %T"`
hostname=`hostname`
# start backup
echo " " >> /data/backup.log 2>&1 &
## mount share_storage
mount -t nfs 10.9.108.228:/UDisk/log_backup_for_mysql /data/mnt
echo " `date +"[%Y-%m-%d %T]"` $hostname incre_backup is start ">> /data/backup.log 2>&1 &
# flush logs and rm binlog  and backup binlog
mysqladmin flush-logs
mysql -e "PURGE MASTER LOGS BEFORE '$Dbinlog'";
rsync -az /data/mysql/log/mysql-bin* /data/mnt/$hostname

echo " `date +"[%Y-%m-%d %T]"` $hostname incre_backup is end ">> /data/backup.log 2>&1 &
