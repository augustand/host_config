global
    log         127.0.0.1 local2

    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    # daemon

    stats socket /var/lib/haproxy/stats

defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    maxconn                 3000

frontend  main *:80
    default_backend             app

backend app
    balance     roundrobin
    {{range $dir := lsdir "/projects"}}
        {{$custdir := printf "/projects/%s/*" $dir}}
        {{range gets $custdir}}
    server {{base .Key}} {{.Value}} check inter 5000 fall 1 rise 2
        {{end}}
    {{end}}


listen status *:8080
    stats enable
    stats uri /stats
    stats auth admin:123456
    stats realm (Haproxy\ statistic)