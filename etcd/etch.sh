#!/usr/bin/env bash

# https://github.com/coreos/etcd/releases

# etcd公共服务
# curl https://discovery.etcd.io/new?size=3
# https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
# 返回值作为启动节点时的 -discovery 参数或者 ETCD_DISCOVERY环境变量的值。


#-name	指定此节点的名字
#-initial-advertise-peer-urls	指定广播给其它节点的此节点地址
#-listen-peer-urls	指定此节点在集群中监听(接受)其它节点通信的地址
#-listen-client-urls	指定用于监听客户端请求的地址
#-advertise-client-urls	指定广播给其它节点的此节点用于监听客户端请求的地址
#-initial-cluster-token	指定此集群的统一token
#-initial-cluster	初始化集群,指定包含所有节点的一个列表
#-initial-cluster-state	初始集群的状态，可以是 (“new” or “existing”)


./etcd --name etcd0 \
	--initial-advertise-peer-urls http://10.1.51.133:2380 \
  	--listen-peer-urls http://10.1.51.133:2380 \
  	--listen-client-urls http://10.1.51.133:2379,http://127.0.0.1:2379 \
  	--advertise-client-urls http://10.1.51.133:2379 \
  	--discovery https://discovery.etcd.io/9c1d9cea74cc9c6f5b34823297b0f558

./etcd --name etcd1 \
 	--initial-advertise-peer-urls http://10.1.51.133:2381 \
  	--listen-peer-urls http://10.1.51.133:2381 \
  	--listen-client-urls http://10.1.51.133:2378,http://127.0.0.1:2378 \
  	--advertise-client-urls http://10.1.51.133:2378 \
  	--discovery https://discovery.etcd.io/9c1d9cea74cc9c6f5b34823297b0f558


./etcd --name etcd2 \
	--initial-advertise-peer-urls http://10.1.51.133:2382 \
  	--listen-peer-urls http://10.1.51.133:2382 \
  	--listen-client-urls http://10.1.51.133:2377,http://127.0.0.1:2377 \
  	--advertise-client-urls http://10.1.51.133:2377 \
  	--discovery https://discovery.etcd.io/9c1d9cea74cc9c6f5b34823297b0f558