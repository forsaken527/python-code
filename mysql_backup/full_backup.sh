# mysql_backup.sh
#!/bin/sh
# define var
rq=` date +"%Y_%m_%d" `
Ddump=`date -d '-7 days' +"%Y_%m_%d"`
Dbinlog=`date -d '-9 days' +"%Y-%m-%d %T"`
hostname=`hostname`
# start backup
echo " " >> /data/backup.log 2>&1 & 
echo " `date +"[%Y-%m-%d %T]"` $hostname full_backup is start ">> /data/backup.log 2>&1 &
# dump
mysqldump --opt --master-data=2 --single-transaction --flush-logs --all-databases > /data/backup/"$hostname"_all_databases_$rq.sql
# mount share_storage
mkdir -p /data/mnt/$hostname
mount -t nfs 10.9.108.228:/UDisk/log_backup_for_mysql /data/mnt
# rm binlog  and backup binlog
mysql -e "PURGE MASTER LOGS BEFORE '$Dbinlog'";
rsync -az /data/mysql/log/mysql-bin* /data/mnt/$hostname
# rm dump and backup 
find /data/backup/ -mtime +8  | xargs rm
rsync -az /data/backup/"$hostname"_all_databases_$rq.sql /data/mnt/$hostname
# rm /data/mnt/"$hostname"
find /data/mnt/"$hostname" -mtime +8 | xargs rm
# end backup
echo " `date +"[%Y-%m-%d %T]"` $hostname full_backup is end ">> /data/backup.log 2>&1 &
