```
input {
    kafka {
        zk_connect => "zk1.dmp.com:2181"
        topic_id => "service-trace"
        group_id => "logstash-service-trace"
        codec => plain
        reset_beginning => true
        consumer_threads => 3
        decorate_events => true
        type => "app-trace"
    }
}

filter {
    if [type] == "service-trace" {
        grok {
            patterns_dir => "/data/dmp/logstash/patterns/service-trace"
            match => {
                "message" => "%{SERVICETRACE}"
            }
        }
        date {
            match => [ "request_time" , "UNIX_MS" ]
        }
    }
}

output {
    elasticsearch {
        hosts => ["host1.elk.freed.so:9200","host4.elk.freed.so:9200","host2.elk.freed.so:9200","host3.elk.freed.so:9200"]
        index => "logstash-%{type}-%{+YYYY.MM.dd}"
        document_type => "%{type}"
        workers => 1
        flush_size => 10
        idle_flush_time => 10
        template_overwrite => true
    }
}

```

**service-trace**
```
SX [^|]*?[|]?
SERVICETRACE    %{UUID:trace_id} \| %{WORD:device_id} \| %{HOSTPORT:node_id} \| 
%{WORD:node_type} \| %{WORD:span_name} \| %{SX:span_id} \| %{SX:pspan_id} \| 
%{NUMBER:request_time} \| %{NUMBER:response_time} \| %{SX:params} \| 
%{SX:result_code:int} \| %{SX:http_status:int} \| %{SX:url} \| %{SX:uid} \| 
%{WORD:protocol} \| %{DATA:annotation} \|
```
