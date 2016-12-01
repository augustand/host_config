# encoding=utf-8

'''
简化版本报告部署脚本
'''

import datetime

from fabric.api import env, run, cd
from fabric.contrib.files import roles, put
from fabric.operations import sudo

# 操作一致的服务器可以放在一组，同一组的执行同一套操作
env.roledefs = {
    'jlog': [
        'centos@192.168.200.178'
    ],
    'test': [
        'centos@192.168.200.178'
    ]
}

env.password = 'centosoffice2015'
env.colorize_errors = True
env.warn_only = True

env.pty = False
env.port = 22
env.parallel = True

# env.skip_bad_hosts = True
# env.timeout = 3

pkill = "ps -ef | grep {} | grep -v grep | awk '{print $2}' | xargs sudo kill -9".format


@roles("jlog")
def jlog_init():
    run("mkdir /home/centos/project")
    with cd("/home/centos/project"):
        run("rm -rf jlog_config")
        run("git clone --depth=1 http://kooksee:12345678@10.1.11.80/python/jlog_config.git jlog_config")
        run('bash jlog_config/Miniconda2-latest-Linux-x86_64.sh -b')
        sudo("sudo yum install nginx")
        run(
            "echo 'export PATH=/home/centos/miniconda2/bin:$PATH' >> /home/centos/.bashrc & source /home/centos/.bashrc")


@roles("jlog")
def jlog_pip():
    run("pip install supervisor")


@roles("jlog")
def jlog_start():
    run("mkdir /home/centos/project")
    with cd("/home/centos/project"):
        run("supervisord -c /home/centos/project/jlog_config/supervisord.conf")
        sudo("sudo nginx -c /home/centos/project/jlog_config/nginx.conf")


@roles("jlog")
def jlog_stop():
    pkill("python")
    pkill("nginx")


# 升级python包
@roles("test_report")
def pip_update():
    with cd("/opt/report/venv/bin"):
        run("./pip list | awk '{print $1}' | xargs ./pip install --upgrade")


# 给所有的服务器上传公钥
@roles("test", "simple_report", "test_service", "test_report")
def sent_ssh_key():
    with cd("~/.ssh"):
        if run("cat ~/.ssh/authorized_keys | grep baiyunhui") != "":
            return

        put("~/.ssh/id_rsa.pub", "~/.ssh/tmp.pub")
        run("cat tmp.pub >> authorized_keys")
        run("rm tmp.pub")


# 线上报告部署
@roles("simple_report")
def online_report_old():
    start_time = datetime.datetime.now()

    with cd("/opt/report"):
        run("rm -rf ./insight")
        run("rm -rf ./dimension_report")
        run(
            "git clone -b productionD_master http://barry:12345678@192.168.200.19/AnalysisTeam/insight.git --depth=1")
        run("mv ./insight/new_report/code/dimension_report .")
        run("cp ./dimension_report/cfg/config_www_productionD.py ./dimension_report/cfg/config.py")

    sudo("sudo restart uwsgi")
    sudo("sudo /etc/init.d/nginx restart")
    sudo("sudo /etc/init.d/celeryd restart")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")

    end_time = datetime.datetime.now()
    print "部署时间为: {}s".format((end_time - start_time).seconds)


@roles("simple_report")
def online_report_new():
    start_time = datetime.datetime.now()

    with cd("/opt/report"):
        run("rm -rf ./insight")
        run("rm -rf ./dimension_report")

        run(
            "git clone http://barry:12345678@192.168.200.19/barry/test_simple.git --depth=1")
        run("mv test_simple insight")

        run("mv ./insight/code/dimension_report .")
        run("cp ./dimension_report/cfg/config_www_productionD.py ./dimension_report/cfg/config.py")

    sudo("sudo restart uwsgi")
    sudo("sudo /etc/init.d/nginx restart")
    sudo("sudo /etc/init.d/celeryd restart")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")

    end_time = datetime.datetime.now()
    print "部署时间为: {}s".format((end_time - start_time).seconds)


@roles("test_report")
def online_report_test():
    start_time = datetime.datetime.now()

    with cd("/opt/report"):
        run("rm -rf ./dimension_report")
        run(simple_report)
        run("mv rpt_simple dimension_report")
        run("cp ./dimension_report/cfg/config_www_productionD_test.py ./dimension_report/cfg/config.py")

    sudo("sudo restart uwsgi")
    sudo("sudo /etc/init.d/nginx restart")
    sudo("sudo /etc/init.d/celeryd restart")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")

    end_time = datetime.datetime.now()
    print "部署时间为: {}s".format((end_time - start_time).seconds)


@roles("simple_report")
def online_report():
    start_time = datetime.datetime.now()

    with cd("/opt/report"):
        run("rm -rf ./dimension_report")
        run(simple_report)
        run("mv rpt_simple dimension_report")
        run("cp ./dimension_report/cfg/config_www_productionD.py ./dimension_report/cfg/config.py")

    sudo("sudo restart uwsgi")
    sudo("sudo /etc/init.d/nginx restart")
    sudo("sudo /etc/init.d/celeryd restart")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")

    end_time = datetime.datetime.now()
    print "部署时间为: {}s".format((end_time - start_time).seconds)


# 测试报告环境部署
@roles("test_report")
def test_report_stop():
    sudo('sudo pgrep nginx | sudo xargs kill -9')
    sudo('sudo pgrep uwsgi | sudo xargs kill -9')
    sudo("sudo stop uwsgi")
    sudo("sudo /etc/init.d/nginx stop")
    sudo("sudo /etc/init.d/celeryd stop")

    sudo("sudo stop uwsgi")
    sudo("sudo /etc/init.d/nginx stop")
    sudo("sudo /etc/init.d/celeryd stop")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")


# 测试报告环境部署
@roles("test_report")
def test_report_start():
    sudo("sudo start uwsgi")
    sudo("sudo /etc/init.d/nginx start")
    sudo("sudo /etc/init.d/celeryd start")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")


# 测试报告环境部署
@roles("test_report")
def test_report():
    start_time = datetime.datetime.now()

    with cd("/opt/report"):
        run("rm -rf ./dimension_report")
        run(simple_report + " -b dev")
        run("mv rpt_simple dimension_report")
        run("cp ./dimension_report/cfg/config_www_productionD_test.py ./dimension_report/cfg/config.py")

    sudo("sudo stop uwsgi")
    sudo("sudo /etc/init.d/nginx stop")
    sudo("sudo /etc/init.d/celeryd stop")

    sudo("sudo start uwsgi")
    sudo("sudo /etc/init.d/nginx start")
    sudo("sudo /etc/init.d/celeryd start")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")

    end_time = datetime.datetime.now()
    print "部署时间为: {}s".format((end_time - start_time).seconds)


# 测试服务报告部署
@roles("test_service")
def test_service():
    start_time = datetime.datetime.now()

    with cd("/opt/services"):
        run("rm -rf data_service")
        run("rm -rf services")

        run(
            "git clone -b productionD_master http://barry:12345678@192.168.200.19/AnalysisTeam/data_service.git --depth=1")
        run("mv ./data_service/services .")
        run("cp ./services/config/config_www_productionD.py ./services/config/config.py")

    sudo("sudo ps aux | grep thrift | grep -v grep | awk '{print $2}' | xargs kill -9")
    run("/opt/services/start_thrift_api.sh")

    sudo("sudo /etc/init.d/nginx restart")
    sudo("sudo restart uwsgi")

    run("pgrep uwsgi | xargs echo")
    run("pgrep nginx | xargs echo")
    run("ps aux | grep thrift | grep -v grep | awk '{print $2}' | xargs echo")

    end_time = datetime.datetime.now()
    print "部署时间为: {}s".format((end_time - start_time).seconds)
