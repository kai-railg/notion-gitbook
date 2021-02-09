# 6 redis-cluster

模拟实现时使用 6 个节点， 三个 master，相当于每个 master 有一个 salve

用 6个配置文件分别开启 6个 redis 服务器

- 修改配置文件

    针对一台服务器的配置

    ```python
    # 后台启动
    daemonize yes
    # 端口号
    port 7001-7006
    # 绑定
    bind 当前机器ip
    # 指定不同的数据目录
    dir /usr/local/redis/data/1-6
    # 开启集群模式
    cluster-enabled yes
    # 集群中的本机状态配置
    cluster-config-filr nodes-7001-6.conf
    # 超时时间
    cluster-node-timeout 5000
    # AOF 持久化
    appendonly yes

    ```

- 安装 ruby

    因为 redis 集群需要 ruby 命令

    yum install ruby rubygems

    gem install redis  (ruby 和 redis 的接口)

- 启动 redis 集群

    分别用配置文件启动 redis 服务器

    切换到 redis 安装目录下的 src 目录，执行命令

    ./redis-trib.rb create —replicas 1  全部的 ip:port 

    —replicas 1 表示 主节点与从节点的比例为1:1，且写在前面的表示主节点，即6台服务中3台主节点，并且按照启动顺序 1 和 4 构成主从关系，2-5 这样。

    ps：在存储数据的过程中，集群会为数据分配槽，并切换到槽所在的redis 服务器上

    ps：数据只在主从中共享，即 keys * 可以查看。但是get 可以查看所有集群中的所有数据

    ps： 当出现集群无法启动时，需要删除临时的数据文件，再次重新启动每一个 redis 服务，然后重新构造集群环境

- 验证 redis 集群

    redis-cli -c -h ip -p port  -c 表示集群模式

    cluster info  查看集群信息

    cluster nodes  查看节点信息

    redis-cli -c -h ip -p port  shutdown  关闭集群某一服务器，关闭集群需逐个关闭redis 服务器

- redis 集群主要命令

    create 创建集群

    fix  单点修复

    check 集群验证

    add-node  添加节点

    del-node  删除节点

    reshard  重新分片

    详情参见 redis 集群文档