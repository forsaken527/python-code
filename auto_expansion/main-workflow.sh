#!/bin/bash

sum=6 #需要创建的host个数
#1. 开始前请确认create_uhost_instance.py中的主机配置!!!!!
#2. 并确认发布系统的war版本
#3. 确认ansible中的hosts与nginx.conf

function create() {
    for ((i=1;i<${sum}+1;i++))
        do
	#开始前请确认create_uhost_instance.py中的主机配置!!!!!
        info=`python create_uhost_instance.py`
        echo $info | awk '{print $2}' >> ip_list
        echo $info | awk '{print $3}' >> id_list
    done
}

function initialize() {
    ##初始化连接
    initialize_ip=$1
    ssh -i /data/etouch/.ssh/id_rsa_root -o 'stricthostkeychecking=no' root@$initialize_ip "hostname"
    #ansible 实例初始化
    echo $initialize_ip >> /etc/ansible/hosts
    ansible $initialize_ip  -m script -a "initialize.sh"
    ssh -i /data/etouch/.ssh/id_rsa_root root@$initialize_ip "cd /data/etouch;sh restart_tomcat.sh 8080"
    ssh -i /data/etouch/.ssh/id_rsa_root root@$initialize_ip "cd /data/etouch;sh restart_tomcat.sh 8081"
    sed -i '/'$initialize_ip'/d' /etc/ansible/hosts   #使用完成后del数据
}

function starting() {
        start_ip=$1
	status=`telnet $start_ip 22 < /dev/null 2>/dev/null | grep '\^' | wc -l`
	if [ $status = 1 ];then
	    initialize $start_ip 
	else
             sleep 30
		status1=`telnet $start_ip 22 < /dev/null 2>/dev/null | grep '\^' | wc -l`
		if [ $status1 = 1 ];then
		    initialize $start_ip
		else
		    sleep 30
		    initialize $start_ip
		fi
	fi
}


function del_uhost(){
    for del_line in $(cat id_list)
        do
        python terminate_uhost_Instance.py $del_line #调用python删除uhost
    done
}

function stop_uhost() {
    for stop_ip in $(cat ip_list)
        do
	#停止服务 关闭uhost
        ssh -i /data/etouch/.ssh/id_rsa_root root@$stop_ip "sh /data/etouch/shutdown_tomcat.sh 8080"
        ssh -i /data/etouch/.ssh/id_rsa_root root@$stop_ip "sh /data/etouch/shutdown_tomcat.sh 8081"
        ssh -i /data/etouch/.ssh/id_rsa_root root@$stop_ip "poweroff"
    done
}

today=`date +"%Y-%m-%d"`
grep $today ucdn_holiday_list
# 有节日
if [ $? -eq 0 ] ;then

    ####
    /bin/rm -fr ip_list id_list
    ###-------create uhost-----#####
    create
    
    ###waiting for started
    sleep 180
    ssh -i /data/etouch/.ssh/id_rsa_root root@api1.pc.freed.so "rsync -avz /data/etouch/8080_tomcat_server/webapps/peacock.war 10.10.199.5::data/tmp/peacock/" 
    ###------instance------#######
    rsync -avz /data/etouch/abcm/hosts/conf/hosts_pc_tc /data/tmp/peacock/hosts #将ansible中的hosts同步到工作目录
    for ip_line in $(cat ip_list)
    do
        starting $ip_line
    done 
    
    ####peacock nginx.conf update
    #同步到当前目录以便于修改
    rsync -az  /data/etouch/abcm/tengine/conf/tengine_pc_tc/conf/nginx.conf ./
    #同步到back目录以便于恢复
    rsync -az /data/etouch/abcm/tengine/conf/tengine_pc_tc/conf/nginx.conf back/
    ####修改当前目录的nginx配置文件
    for read_ip in $(cat ip_list) 
    do
        service8080="server ""${read_ip}"":8080;"
        service8081="server ""${read_ip}"":8081;"
        sed -i "/server api7.pc.freed.so:8081;/a\        $service8080"  nginx.conf
        sed -i "/server api7.pc.freed.so:8081;/a\        $service8081"  nginx.conf
    done
    ####将修改后的配置文件同步到ansible配置中,并同步
    rsync -az nginx.conf /data/etouch/abcm/tengine/conf/tengine_pc_tc/conf/
    /bin/sh /data/etouch/abcm/tengine/main_pc_tc.sh
    ######wait for hoilday end!
    sleep 80m
    ####stop and del uhost
    ##recover
    stop_uhost
    sleep 30
    del_uhost
    rsync -avz back/nginx.conf /data/etouch/abcm/tengine/conf/tengine_pc_tc/conf/
    /bin/sh /data/etouch/abcm/tengine/main_pc_tc.sh
    /bin/rm -fr id_list ip_list 
fi
