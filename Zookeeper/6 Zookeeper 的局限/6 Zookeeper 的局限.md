# 6 Zookeeper 的局限

- 将所有的信息放到内存中操作，服务器的内存大小决定了znode节点所能够的存储的数据量的大小
- 支持读多写少的场景，增加机器可以提升ZK的读性能，但写性能会降低
    - 原因是写操作需要集群中超过半数的机器投票决定
- 不能迁移
    - 无法自动完成的系统版本的切换和迁移
- 只允许奇数节点
- 增加新的ZK服务器可能会导致数据不一致
    - 当新的ZK节点超过旧的节点时，新服务器会形成仲裁
- Multi-Paxos 比较复杂且太过理论化