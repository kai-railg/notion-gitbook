# change buffer

- 当需要更新一个数据页时，如果数据页在内存中，就直接更新。
- 如果不在内存中，在不影响数据一致性的前提下，InnoDB会将这些`更新操作缓存在内存`中，即 change buffer。这样就不需要从磁盘中读取数据了。在下次需要访问这个数据时，将数据页读入内存，再进行 change buffer 与 磁盘的merge操作。
- change buffer 也是可以持久化的数据。
- 将 change buffer 中的操作应用到原数据页的过程，成为`merge`。除了访问数据页会触发merge，系统后台也会定期merge，以及在shutdown前执行merge。
- 将更新操作记录在chaneg buffer中，可以有效提示语句的执行速度。并且读取磁盘中的数据到内存中也会占用内存，两者相比较而言`change buffer更节省内存`。
- change buffer的使用条件
    - 只有普通索引才可以用change buffer。
    - change buffer不具备判断数据唯一性的约束，因此不适用唯一索引。
        - 判断唯一性需要先判断表中是否存在该字段，需要把该数据页从磁盘读取到内存中，因为`change buffer就失去了意义`。
- change buffer的使用场景
    - change buffer对`写多读少`的场景可以起到明显的加速作用。
        - 因为change buffer是将更新操作缓存下来，然后统一merge到磁盘，因为写操作越多效率提升就越高。
    - 常见的就是账单类、日志类系统
    - 要求读少的原因
        - 因为写完马上就读的话，需要从磁盘去查询数据，然后进行change buffer的merge。读频繁的话，不但IO次数不会减少，反而增`加change buffer 的维护成本。`
- `change buffer主要节省的是随机读磁盘的IO收益`。
- meger的流程
    1. 从磁盘读到旧的数据
    2. 合并change buffer和旧的数据，得到最新的数据页
    3. 写redo log。redo log 包含数据的变更和change buffer的变更
    - merge的流程就结束了，数据页还没有刷新到磁盘中，属于脏页。之后会刷新到磁盘