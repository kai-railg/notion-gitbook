# MySQL选择索引的逻辑

- 选择索引是优化器的工作，优化器选择索引的目的，就是发现一个`最优的执行方案`，并用最小的代价去执行语句。
- MySQL，`扫描行数`是影响执行代价的因素之一。扫描的行数越少，意味着访问磁盘数据的次数越少，消耗的CPU资源越少。
    - 优化器也会结合`是否使用临时表`、`是否排序`来综合判断。
- 扫描行数怎么判断的
    - MySQL真正开始执行前，并不知道具体的行数有多少，而只能根据`统计信息`来估计记录数
        - 统计信息就是索引的`区分度`。
            - 一个索引上不同的值越多，区分度就越好。
            - 而索引上不同的值的个数，称为`基数`。基数越大，区分度就越好。
            - `show index from table;`   查看索引和索引的基数
    - MySQL获得索引基数的方法
        - 采样统计
            - 统计N个数据页的不同值，得到一个平均值。然后乘以这个索引的页数，就得到索引的基数。即随机取样方法。
                - 比如N=3，第一个页面20，第二个页面15，第三个页面10，平均值为10，10*索引的页数就是基数。N默认20或10。
        - 数据表更新过程中，当变更的数据超过1/M，M默认10或16。
    - 索引基数虽然不够准确，但是大体上是差不多的。
    - 获取索引基数后，分析器还要`预估一个扫描行数`的值。
        - `explain select * from table;`
            - 返回的rows 即时预估的值。
    - 预估扫描行数后，还要考虑`回表的成本` 和`标记删除`。
        - 比如普通索引预估扫描行数5W行，主键索引预估10W行，那么MySQL就会选择主键索引的10W行。
        - 因为还要考虑到并发的事务，删除的数据可能只是标记删除，数据仍然在数据页上。后插入的数据需要寻找空位插入，这样`查询时会扫描删除的事务+后插入的数据，同时还要加上回表`。
- 通过 `analyze table t;` 可以获取正确的扫描行数
- 索引异常和处理
    - force index 强行选择索引
        - select * from t force index(a) where a between 10000 and 20000;
    - 新建一个更合适的索引
    - 删除掉会导致选择错误的索引
-