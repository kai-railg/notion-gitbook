# MySQL的主备

binlog 不仅可以用来归档，也可以用来做主备同步

几乎MySQL所有的高可用架构，都是从一主一备演化来的，基本都离不开binlog

- 主备架构
    - M-S   master-slave  一主一备或多备
    - M-M   master-master  总是互为主备，不需要额外切换
- 主备基本原理
    - 一主一备中，主库响应客户端的访问，备库同步主库的更新即可。
    - 当要切换的时候，主备的身份切换一下即可。
    - 一般情况下都把备库设置为readonly
        - 可以防止运营类的误操作
        - 防止切换逻辑产生bug，造成主备数据不一致
        - 可以用readonly 的状态，判断节点的角色
    - `readonly 对 super 权限是无效的`，而备库的更新操作都是使用 super权限
    - 数据同步的流程
        - 主库接受更新请求，同时正常写入 redo log和 binlog
        - 主库和备库维持一个长连接，主库内部有一个线程，专门服务和备库的长连接
        - 首先在备库上执行 change master 命令，设置主库的身份信息，以及binlog 的位置，位置包含文件名和日志偏移量
        - 在备库上执行 start slave 命令，备库会启动两个线程
            - io_thread  负责与主库进行连接
            - sql_thread  SQL解析线程，由单线程演化为多线程
        - 主库校验备库的身份，按照备库要求的位置从本地读取binlog进行传输
        - 备库拿到binlog，写入本地文件，称为中转日志 relay log
        - sql_thread 读取日志，解析命令并执行
- binlog 的三种格式
    - statement
        - 记录的`语句原文`，是unsafe的，因为在主备同步时会出现数据不一致的情况
            - `mysql> delete from t where a>=4 and t_modified<='2018-11-10' limit 1;`
            - 主库里用的可能是a索引，备库里可能用的是t_modified索引，加上limit的情况就可能会导致错误
    - row
        - 需要mysqlbinlog工具查看row格式的日志
        - binlog里记录的是真是删除的行的主键ID，不会出现主备不一致的情况
        - 但是row会特别占空间，比如删除10000行记录，就要记录100000行
    - mixed
        - 针对statement会出现数据不一致的情况，row占空间的情况，采取的折中方案
        - mixed 是MySQL会判断这条SQL是否会出现主备不一致的情况，如果不会，就是用statement，否则就是用row格式
        - mixed 利用statement的优点，又避免数据不一致的情况
    - 推荐row格式，因为有个额外的场景：`恢复数据`
        - 恢复数据时会把delete、insert语句互相转化
        - update 语句则是记录前后的值
- 循环复制问题
    - M-M架构时，节点互为主备，binlog在会在节点互相传递，不断的执行语句，就是循环复制
    - MySQL会在binlog中记录第一个执行所在实例的server id，并做如下规定
        - 两个库server id必须不同，否则不能成为主备关系
        - 一个备库接到binlog并同步时，生成与原binlog的server id相同的新的binlog
        - 每个库在收到自己的主库的binlog时，会判断server id与自己是否相同，相同就直接丢弃
    -