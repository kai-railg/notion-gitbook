# 4 Zookeeper 使用文档

- [zkServer.sh](http://zkserver.sh/)   start | stop | status   服务启动和管理
- [zkCli.sh](http://zkcli.sh)  进入客户端
    - create  /app1 创建znode
    - ls -R /   查看根信息
    - get  /app1   查看znode
    - delete /app1  删除znode
- Python 通过 kazoo 与 zookeeper 交互
- JAVA 通过 curator 交互