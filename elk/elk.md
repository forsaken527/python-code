##版本


|project|version|
|:------|:------|
|elasticsearch|2.4.0|
|kibana|4.6.2
|logstash|2.4.1|

##系统环境要求
+ 用户
```
groupadd -g 555 dmp;useradd -g 555 -u 555 -d /data/dmp dmp
```
+ jvm内存设定
```
ES_HEAP_SIZE=8g
```
+ 禁用swap
```
swapoff -a #或者直接删除fstab的mount
```
+ jdk
```
java version "1.8.0_111"  #以便于后续对5.0的升级
```
+ MMap
```
sysctl -w vm.max_map_count=655300
systtc -p
```
+ 其他内核参数以及最大文件句柄数等
```
#limits.conf
	work soft nofile 819200
	work hard nofile 819200
	dmp soft memlock unlimited
	dmp hard memlock unlimited
#90-nproc.conf
    *	soft    nproc     unlimited
```
+ hosts
```
# kafka cluster
10.10.95.71     kafka1.dmp.com
10.10.22.251    kafka2.dmp.com
10.10.52.152    kafka3.dmp.com
# kafka hosts
10.10.95.71    10-10-95-71
10.10.52.152   10-10-52-152
10.10.22.251   10-10-22-251
# zk cluster
10.10.95.131    zk1.dmp.com
10.10.34.92     zk2.dmp.com
10.10.48.188    zk3.dmp.com
#以及elk集群的hosts
```

+ 启动脚本

```shell
#!/bin/sh

export ES_HEAP_SIZE=10g
bin/elasticsearch -d

```

##配置文件
```config
cluster.name: etouch-elk
node.name: host1.elk.freed.so
path.data: /data1,/data2,/data3,/data4,/data5,/data6 #多个存储路径以提高io
path.logs: /data/dmp/elasticsearch/logs
bootstrap.mlockall: true  #锁定内存,同时也要允许elasticsearch的进程可以锁住内存
network.host: host1.elk.freed.so
http.port: 9200
discovery.zen.ping.unicast.hosts: ["host2.elk.freed.so","host3.elk.freed.so"]
discovery.zen.ping.multicast.enabled: false #禁止当前节点发现多个集群节点，默认值为true
discovery.zen.minimum_master_nodes: 3  #构成集群最小实例个数
gateway.recover_after_nodes: 3 #N/2+1
node.max_local_storage_nodes: 1 #禁止从单个目录启动多个实例
action.destructive_requires_name: true
#index.number_of_shards: 5 #数据分片数，数据分片用于设置index最终切分的个数
#index.number_of_replicas: 1  #数据副本数，数据分片数用于设置index中数据重复的个数
```

###logstash相关配置文件
####nginx-access相关
* logstash => kafka

```config
input {
    file {
        path => "/data/etouch/nginx/log/kmtask.access.log-*"
        codec => json
        start_position => "beginning"
    }
}

output {
    kafka {
        bootstrap_servers => "kafka1.dmp.com:9092"
        topic_id => "80-client-lz.rili.cn"
        codec => plain {
            format => "%{message}"
        }
    }
}
```
* kafka => logstash => es

**当从kafka数据的时候,将`group_id`设定为`logstash-${type}`，`type`的值为es中的`index`的`type`**

```config
input {
    kafka {
        zk_connect => "zk1.dmp.com:2181"
        topic_id => "80-client-lz.rili.cn"
        group_id => "logstash"
        codec => plain
        reset_beginning => false
        consumer_threads => 3
        decorate_events => true
        type => "nginx-access"
    }
}

filter {
    if [type] == "nginx-access" {
        grok {
            patterns_dir => "/data/dmp/logstash/patterns/nginx-access"
            match => {
                    "message" => "%{NGINXACCESS}"
            }
        }
        date {
            match => [ "time_locale" , "dd/MMM/yyyy:HH:mm:ss Z" ]
        }
        ruby { code => "event['http_x_forwarded_for'] = event['http_x_forwarded_for'].split(',')" }
        geoip {
            source => "http_x_forwarded_for"
            target => "geoip"
            database => "/data/dmp/logstash/conf/GeoLiteCity.dat"
        }
    }
}


output {
    elasticsearch {
        hosts => ["host1.elk.freed.so:9200","host2.elk.freed.so:9200","host3.elk.freed.so:9200"]
        index => "logstash-%{type}-%{+YYYY.MM.dd}"
        document_type => "%{type}"
        workers => 1
        flush_size => 10
        idle_flush_time => 10
        template_overwrite => true
    }
}
#patterns
SX [^|]*?[|]?
NGINXACCESS     \[%{HTTPDATE:time_locale}\] \|%{SX:remote_user} \|%{SX:remote_addr} \| %{SX:http_x_forwarded_for} \|%{SX:node_type} \|%{SX:ip-port} \|%{SX:domain} \|%{SX:request} \|%{SX:status} \|%{SX:body_bytes_sent} \|%{SX:request_time} \|%{SX:upstream_response_time} \|%{SX:http_referer} \|%{SX:http_user_agent} \|%{SX:request_body} \|%{SX:http_t_trace_id} \|%{SX:http_t_device_id} \|%{SX:http_t_next_span} \|%{SX:http_t_parent_id} \|%{SX:http_t_uid} \|

```

####mysql_slow

```
input {
    file {
        type => "mysql-slow"
        path => "/data/mysql/log/slow.log"
        close_older => "360000"
        codec => multiline {
            pattern => "^# User@Host:"
            negate => true
            what => "previous"
        }
    }
}
filter {
    grok {
        match => [ "message", "(?m)^# User@Host: %{USER:user}\[[^\]]+\] @ (?:(?<clienthost>\S*) )?\[(?:%{IP:clientip})?\]\s*\n# Query_time: %{NUMBER:query_time
:float}\s+Lock_time: %{NUMBER:lock_time:float}\s+Rows_sent: %{NUMBER:rows_sent:int}\s+Rows_examined: %{NUMBER:rows_examined:int}\s*(?:use %{DATA:database};\s*)
?SET timestamp=%{NUMBER:timestamp};\s*\n(?<query>(?<action>\w+)\s+.*)\n# Time:.*$" ]
    }
    date {
        match => [ "timestamp", "UNIX" ]
        remove_field => [ "timestamp" ]
  }
}



output{
    elasticsearch {
        hosts => ["host1.elk.freed.so:9200","host2.elk.freed.so:9200","host3.elk.freed.so:9200"]
        index => "logstash-%{type}-%{+YYYY.MM.dd}"
        document_type => "%{type}"
        workers => 1
        flush_size => 10
        idle_flush_time => 10
        template_overwrite => true
    }
}
```

####tomcat-log
```
input {
    file {
        path => [
            "/data/etouch/8080_tomcat_server/logs/pc-or-pcstats.suishenyun.net-log4j/log.txt",
            "/data/etouch/8081_tomcat_server/logs/pc-or-pcstats.suishenyun.net-log4j/log.txt"
        ]
        type => "log4j-json"
        start_position => "beginning"
        codec => json
    }
}

output {
	elasticsearch {
    	hosts => ["host1.elk.freed.so:9200","host2.elk.freed.so:9200","host3.elk.freed.so:9200"]
        index => "logstash-%{type}-%{+YYYY.MM.dd}"
        document_type => "%{type}"
        workers => 1
        flush_size => 10
        idle_flush_time => 10
        template_overwrite => true
    }
}
```




###一些其他的优化内容
1. 当不需要很高的实时性，需要更高的写入性能,可以适当提高写入的频率`refresh_interval`
```html
curl -XPOST http://127.0.0.1:9200/logstash-2015.06.21/_settings -d'
{
	"refresh_interval": "10s" ,
   }'
```
2. 归并线程的限速配置 `indices.store.throttle.max_bytes_per_sec`,default=20M,将零散的segment做数据归并，尽量让索引内只有少量的，每个较大的segment文件。这个过程是有独立的进程进行的，并不影响新segment的产生，segment归并的过程，需要先读取segment，归并计算，再将多个小segment写成一个大的segment，最后刷新到磁盘。可以适当调整限速，增大阈值到100M左右，ssd或者高转速磁盘可以更高
```html
curl -XPUT http://127.0.0.1:9200/_cluster/settings -d '
{
    "persistent" : {
        "indices.store.throttle.max_bytes_per_sec" : "100mb"
    }
}'
```
3. 归并线程的数量，cpu核心数的一半，当感觉磁盘性能跟不上的时候可以适当降低：
```language
index.merge.scheduler.max_thread_count  6
```
4. 归并策略配置
```language
index.merge.policy.floor_segment  默认 2MB，小于这个大小的 segment，优先被归并。
index.merge.policy.max_merge_at_once  默认一次最多归并 10 个 segment
index.merge.policy.max_merge_at_once_explicit  默认 optimize 时一次最多归并 30 个 segment。
index.merge.policy.max_merged_segment  默认 5 GB，大于这个大小的 segment，不用参与归并。optimize 除外。
```
5. 当有一个巨大的数据索引存入时，超过了index.merge.policy.max_merged_segment的阈值，就必然会有为数不少的 segment 永远存在，这对文件句柄，内存等资源都是极大的浪费，而是在负载较低的时候使用通过 optimize 接口，强制归并segment
```language
curl -XPOST http://127.0.0.1:9200/logstash-2 ... ? max_num_segments=1
```
** 绝对不建议对还在写入数据的热索引执行这个操作**

6. 动态调整副本配置，而不能动态调整主分片，从而导致取余的分母变化，最终导致数据不可读，大得segment，可以先去除副本，等待optimize完成后，再开启副本
```language
curl -XPUT http://127.0.0.1:9200/logstash-mweibo-2015.05.02/_settings -d '{
    "index": { "number_of_replicas" : 0 }
}'
```

7. 节点用于 fielddata 的最大内存，如果 fielddata 达到该阈值，就会把旧数据交换出去。默认设置是不限制，强烈建议开启，例如为10%百分数或者为绝对值
```language
indices.fielddata.cache.size：50mb
```

8. 节点控制
```language
# 1、以下列出了三种集群拓扑模式，如下:
# 如果想让节点不具备选举主节点的资格，只用来做数据存储节点。
node.master: false
node.data: true
# 2、如果想让节点成为主节点，且不存储任何数据，只作为集群协调者。
node.master: true
node.data: false
# 3、如果想让节点既不成为主节点,又不成为数据节点,那么可将他作为搜索器,从节点中获取数据,生成搜索结果等
node.master: false
node.data: false
```

9. 索引相关
```language
# 设置索引的分片数,默认为5  "number_of_shards" 是索引创建后一次生成的,后续不可更改设置
index.number_of_shards: 5
# 设置索引的副本数,默认为1
index.number_of_replicas: 1
#索引刷新频率，太频繁，新的数据写入变慢，
index.refresh_interval: 120s
```

10. translog
```language
#当事务日志累积到多少条数据后flush一次。
index.translog.flush_threshold_ops: 50000
```



##集群节点添加

+ 新添加的节点配置文件
```config
cluster.name: etouch-elk
node.name: host4.elk.freed.so
path.data: /data/dmp/elasticsearch/data
path.logs: /data/dmp/elasticsearch/logs
bootstrap.mlockall: true
network.host: host4.elk.freed.so
http.port: 9200
discovery.zen.ping.unicast.hosts: ["host1.elk.freed.so","host2.elk.freed.so","host3.elk.freed.so"] #此处需要配置原来集群中的所有节点
discovery.zen.ping.multicast.enabled: false
discovery.zen.ping.timeout: 10s
discovery.zen.minimum_master_nodes: 3
gateway.recover_after_nodes: 3
node.max_local_storage_nodes: 1
```
