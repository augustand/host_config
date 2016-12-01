#!/usr/bin/env bash

if [ $1 = 'init' ]; then
    mkdir $HOME/project
    git clone http://kooksee:12345678@10.1.11.80/python/jlog_config.git $HOME/project/jlog_config --depth=1
    bash $HOME/project/jlog_config/Miniconda2-latest-Linux-x86_64.sh -b
    echo 'export PATH=$HOME/miniconda2/bin:$PATH' >> $HOME/.bashrc
    source $HOME/.bashrc

    pip install supervisor
    sudo yum install nginx
fi

if [ $1 = 'nginx' ]; then
    sudo nginx -c $HOME/project/jlog_config/nginx.conf
fi

if [ $1 = 'supervisor' ]; then
    supervisord -c $HOME/project/jlog_config/supervisord.conf
fi

if [ $1 = 'renginx' ]; then
    ps -ef | grep nginx | grep -v grep | awk '{print $2}' | xargs sudo kill -9
    ps -ef | grep nginx | grep -v grep

	sudo nginx -c $HOME/project/jlog_config/nginx.conf
	ps -ef | grep nginx | grep -v grep
fi

if [ $1 = 'resupervisor' ]; then
    ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs sudo kill -9
    ps -ef | grep python | grep -v grep

	supervisord -c $HOME/project/jlog_config/supervisord.conf
	ps -ef | grep python | grep -v grep
fi

if [ $1 = 'help' ]; then
    echo "
    init 初始化
    nginx 启动nginx
    supervisor 启动supervisor
    renginx 重启renginx
    resupervisor 重启resupervisor
    "
fi

