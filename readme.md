# 系统环境配置
> git clone http://kooksee:12345678@10.1.11.80/python/jlog_config.git $HOME/project/jlog_config --depth=1

1. python安装
系统python环境版本和依赖包需要sudo安装，容易产生权限问题
```
bash $HOME/project/jlog_config/Miniconda2-latest-Linux-x86_64.sh -b
echo 'export PATH=$HOME/miniconda2/bin:$PATH' >> $HOME/.bashrc
source $HOME/.bashrc
```

2. 安装supervisor
```
pip install supervisor
supervisord -c $HOME/project/jlog_config/supervisord.conf
ps -ef | grep supervisord | grep -v grep | awk '{print $2}' | xargs sudo kill -9
ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs sudo kill -9
```

3. 安装nginx
```
sudo yum install nginx
sudo nginx -c $HOME/project/jlog_config/nginx.conf
ps -ef | grep nginx | grep -v grep | awk '{print $2}' | xargs sudo kill -9
```

4. 生成项目目录
```
mkdir $HOME/project
```

5. 启动管理
```
新系统，先初始化
bash manage.sh help
bash manage.sh init
```


