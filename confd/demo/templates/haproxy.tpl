global
    log 127.0.0.1 local3 info
    maxconn 4096
    daemon
    nbproc 1
    # pidfile /usr/local/haproxy/logs/haproxy.pid

defaults
    maxconn 2000
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    mode http
    log global
    log 127.0.0.1 local3 info
    stats uri /admin?stats
    option forwardfor

frontend http_server
    bind :8080
    log global
    default_backend app

backend app
    balance     roundrobin
	{{range $dir := lsdir "/projects"}}
        {{$custdir := printf "/projects/%s/*" $dir}}
        {{range gets $custdir}}
    server {{base .Key}} {{.Value}} check inter 5000 fall 1 rise 2
        {{end}}
    {{end}}

