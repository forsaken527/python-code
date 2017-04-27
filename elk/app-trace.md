```
input {
   kafka {
        zk_connect => "zk1.dmp.com:2181"
        topic_id => "app-trace"
        group_id => "logstash-app-trace"
        codec => plain
        reset_beginning => true
        consumer_threads => 3
        decorate_events => true
        type => "app-trace"
    }
}

filter {
    if [type] == "app-trace" {
        grok {
            patterns_dir => "/data/dmp/logstash/patterns/app-trace"
            match => {
                "message" => "%{APPTRACE}"
            }
        }
        date {
            match => [ "time_locale" , "dd/MMM/yyyy:HH:mm:ss Z" ]
        }
        ruby {
            init => "@some = ['response_time','span_name','url','trace_id','http_status','node_id','protocol','request_time','node_type','span_id','device_id','result
_code','uid','params','pspan_id']"
            code => "
                new_event = LogStash::Event.new(Hash[@some.zip(event.get('request_body').split('&'))])
                new_event.remove('@timestamp')
                event.append(new_event)
            "
        }
        if [span_name] {
            kv {
                source => "span_name"
                field_split => "="
            }
        }
        if [response_time] {
            kv {
                source => "response_time"
                field_split => "="
            }
        }
        if [url] {
            kv {
                source => "url"
                field_split => "="
            }
        }
        if [trace_id] {
            kv {
                source => "trace_id"
                field_split => "="
            }
        }
        if [http_status] {
            kv {
                source => "http_status"
                field_split => "="
            }
        }
        if [node_id] {
            kv {
                source => "node_id"
                field_split => "="
            }
        }
        if [protocol] {
            kv {
                source => "protocol"
                field_split => "="
            }
        }
        if [node_type] {
            kv {
                source => "node_type"
                field_split => "="
            }
        }
        if [span_id] {
            kv {
                source => "span_id"
                field_split => "="
            }
        }
        if [device_id] {
            kv {
                source => "device_id"
                field_split => "="
            }
        }
        if [result_code] {
            kv {
                source => "result_code"
                field_split => "="
            }
        }
        if [uid] {
            kv {
                source => "uid"
                field_split => "="
            }
        }
        if [params] {
            kv {
                source => "params"
                field_split => "="
            }
        }
        if [pspan_id] {
            kv {
                source => "pspan_id"
                field_split => "="
            }
        }
        if [request_time] {
            kv {
                source => "request_time"
                field_split => "="
            }
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

APPTRACE
```
SX [^|]*?[|]?
APPTRACE %{IP:remote_addr} \| %{IP:server_addr} \- \[%{HTTPDATE:time_local}\] \| \"%{SX:request}\" \| %{NUMBER:status} \| %{NUMBER:body_bytes_sent} \| %{SX:http_referer} \| \"%{SX:http_user_agent}\" \| %{SX:http_x_forwarded_for} \| %{SX:request_body} \| %{NUMBER:request_time} \| %{NUMBER:upstream_response_time:float}
```
