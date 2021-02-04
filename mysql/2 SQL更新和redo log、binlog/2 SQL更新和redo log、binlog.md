# SQL和更新和redo log、binlog

- redo log
    - redo log
        - 更新操作会遇到的问题
            - 如果每次更新操作都需要写进`磁盘`，然后找到对应的那条记录，再执行更新操作，整个过程的`IO成本`会很高。
        - MySQL的`WAL`技术
            - Write-Ahead Logging，关键点是`先写日志`，`再写磁盘`。用来解决IO成本过高的问题。
            - 当有一条记录需要更新时，InnoDB 会先把记录写到redo log中，并更新内存，这个更新就算完成了。InnoDB在适当的时候再把内存中这个记录刷新到磁盘中。
        - redo log 是InnoDB独有的日志，大小固定，采用循环写的模式，不具备持久化能力。
            - 比如 redo log大小4GB，写满后会重头开始写
            - `check point` 是开头的位置，也是开始擦除的位置
            - `write pos` 是当前记录的位置，也就是redo log当前结尾的位置
            - 当write pos追上check point时，就得停下来擦除一些内容 check point 向前推进

                ![SQL%E5%92%8C%E6%9B%B4%E6%96%B0%E5%92%8Credo%20log%E3%80%81binlog%20a0f24b3bb42e4ffcbd75107a72af67c7/Untitled.png](SQL%E5%92%8C%E6%9B%B4%E6%96%B0%E5%92%8Credo%20log%E3%80%81binlog%20a0f24b3bb42e4ffcbd75107a72af67c7/Untitled.png)

        - redo log确保了即使数据库发生异常重启，之前提交的记录也不会丢失。
            - 这个能力成为 `crash-safe`
- binlog
    - redo log是InnoDB特有的日志模块，属于引擎层的日志
    - 而`Server层`也有自己的日志，就是`binlog`
    - 为什么会有两份日志？
        - 最初MySQL的默认引擎是`MyISAM`，但是MyISAM没有crash-safe的能力，binlog只能用于`归档`。
        - redo log用来实现crash-safe 能力。
    - redo log 和binlog的区别
        - redo log只能InnoDB使用； binlog 所有引擎都可以使用
        - redo log是物理日志，记录的是在某个数据页做了哪些修改（用于同步磁盘数据）；binlog是逻辑日志，记录的是在某一行上执行了什么操作（用于恢复磁盘数据）
        - redo log是循环写的，空间固定会用完；binlog是追加写的，具有持久性
    - 所以一条SQL语句的更新流程可以简单理解为
        - 查找行记录 → 修改行数据 → 更新数据到内存中 → 写入 redo log(prepare状态) → 写入 binlog → 提交事务 → 修改redo log为commit状态
        - redo log的prepare和commit的两个状态称为两阶段提交。
    - 两阶段提交
        - 如果`不使用`两阶段提交会发生什么
            - 先写 redo log 后写 binlog，如果redo log写完crash，binlog恢复的数据就会缺失
            - 先写 binlog 后写 redo log，如果binlog写完crash，redo log恢复的数据就会缺失
        - 导致的问题就是数据库的状态可能和用它的日志恢复出来的库的`状态不一致`
    - 持久化的设置
        - `innodb_flush_log_at_trx_commit` 设置成1，表示每次事务的redo log都会刷新到磁盘
        - `sync_binlog` 设置成1，表示每次事务的binlog都会刷新到磁盘

        ![SQL%E5%92%8C%E6%9B%B4%E6%96%B0%E5%92%8Credo%20log%E3%80%81binlog%20a0f24b3bb42e4ffcbd75107a72af67c7/Untitled%201.png](SQL%E5%92%8C%E6%9B%B4%E6%96%B0%E5%92%8Credo%20log%E3%80%81binlog%20a0f24b3bb42e4ffcbd75107a72af67c7/Untitled%201.png)