```
input {
    kafka {
        zk_connect => "zk1.dmp.com:2181"
        topic_id => "nginx-trace"
        group_id => "logstash-nginxi-trace"
        codec => plain
        reset_beginning => true
        consumer_threads => 3
        decorate_events => true
        type => "nginx-trace"
    }

}


filter {
    if [type] == "nginx-trace" {
        grok {
            patterns_dir => "/data/dmp/logstash/patterns/nginx-trace"
            match => {
                "message" => "%{NGINXTRACE}"
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
```

NGINX-TRACE
```
SX [^|]*?[|]?
NGINXTRACE    \[%{HTTPDATE:time_locale}\] \| %{SX:remote_user} \| 
%{SX:remote_addr} \| %{SX:http_x_forwarded_for} \| %{SX:node_type} \| 
%{SX:ip-port} \| %{SX:domain} \| %{SX:request} \| %{SX:status:int} \| 
%{SX:body_bytes_sent:int} \| %{SX:request_time:float} \| 
%{SX:upstream_response_timei:float} \| %{SX:http_referer} \| 
%{SX:http_user_agent} \| %{SX:request_body} \| %{SX:http_t_trace_id} \| 
%{SX:http_t_device_id} \| %{SX:http_t_next_span} \| %{SX:http_t_parent_id} \| 
%{SX:http_t_uid} \|
```
