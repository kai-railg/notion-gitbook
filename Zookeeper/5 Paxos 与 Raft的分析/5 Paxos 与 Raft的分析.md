# 5 Paxos 与 Raft的分析

- Raft 算法
    - Raft
        - Raft 是一种用来替代 Paxos 的共识算法。
        - Raft 的目标是提供更清晰的逻辑分工使得算法本身能被更好的理解
        - Raft 能为在计算机集群之间部署有限状态机提供一种通用方法，并确保集群内的任意节点在某种状态转化上保持一致。
    - 简介
        - Raft 通过选举领袖的方式做共识算法。
        - 在 Raft 集群中，服务器可能会是这三种身份之一： 领袖 Leader、追随者 follower、候选人 candidate。
        - 在正常情况下，只有一个 Leader，其他都是 follower。leader 会负责所有外部的请求，如果不是 leader 的机器收到时，请求会被转到 leader
        - leader 定时会发送心跳信息，如果追随者超时没有收到心跳信息，就会进行选举
        - Raft 将问题拆成子问题分开解决
            - 领袖选举 Leader Election
            - 记录复写 Log Replication
            - 安全性 Safety
    - 领袖选举 Leader Election
        - 当 集群启动或者leader 异常的时候，需要选举出新的leader
        - 选举由 候选人发起，follower 会把自己的任期编号 +1、宣布竞选、投自己一票、并向其他服务器拉票，并且每个 follower 只能投1票
        - 任期编号小的follower会自动落选，称为 任期编号大的 follower
    - 记录复写
        - 记录复写 由 leader 来记录
        - 整个集群有复写的状态机，可用来执行外部指令。leader 接受指令并记录，然后转发命令给 follower，直到每个 follower都成功将指令写入记录
        - 当 leader 收到半数follower的确认写入消息时，就会在状态机上执行该指令
        - 当 leader 异常时，新的leader 会同步这个记录
    - 安全性
        - 选举安全性   每个任期最多只能选举一个leader
        - 领袖附加性   leader会把新指令记录在记录尾端，不会改写或删除
        - 记录符合性  如果某个指令在两个记录中的任期和指令序号一样，则保证序号较小的指令也完全一样
        - 领袖完整性 如果某个指令在某个任期中存储成功，则保证存在于领袖该任期之后的记录中
        - 状态机安全性  如果某服务器在其状态机上运行了某个指令，其他服务器保证不会在同个状态上运行不同的指令
- Raft 与 Multi-Paxos的区别
    - Raft 是基于对 Multi-Paxos 的两个限制形成的
    1. 发送的请求是连续的，Raft的appendg操作必须是连续的，而Paxos是并发的
    2. Raft 选主有限制，必须包含最新的、最全日志的才能被选为leader
    - Raft 可以看作是Multi-Paxos的简版
    - Multi-Paxos允许并发的写log,当leader节点故障后，剩余节点有可能都有日志空洞。所以选出新leader后, 需要将新leader里没有的log补全,在依次应用到状态机里
- `[参考文档](https://www.zhihu.com/question/36648084/answer/82332860)`