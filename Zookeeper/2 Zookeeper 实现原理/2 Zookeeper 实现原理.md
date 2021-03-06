# 2 Zookeeper 实现原理

- Paxos 共识算法
    - `[Wiki链接](https://zh.wikipedia.org/zh-cn/Paxos%E7%AE%97%E6%B3%95)`
    - 基于消息传递通信模型的分布式系统，不可避免的会遇到以下问题： 进程可能会变慢、被杀死或者重启，消息可能会延迟、丢失、重试，在不考虑`拜占庭错误`的情况，Paxos解决的是一个可能会发生以上异常的分布式系统如何保持某个值的一致，且不论发生任何异常，都不会破坏决议的共识。
    - Paxos 基于两阶段提交并扩展，算法的特点
        - 只要超过半数的节点存活且可以互相通信，那么整个系统就可以达成一致
        - 最多只能对一个提案达成一致
        - 系统针对所有提案的某个提案必须达成一致
        - 一个或多个节点可以提出提案
    - 案例
        - 有A1、A2、A3、A4、A5 五位议员，议员A1发出一个草案
            - 现有的税率是什么?如果没有决定，我来决定一下. 提出时间：本届议会第3年3月15日;提案者：A1
        - 在最简单的情况下，没有人竞争，于是A2-A5回应
            - 我已收到你的提案，等待最终批准
        - 而A1在收到2份回应后
            - 税率已定为10%,新的提案不得再讨论本问题。
        - 现在我们假设一个复杂的情况，A1提出草案的同时，A5提出
            - 现有的税率是什么?如果没有决定，我来决定一下.时间：本届议会第3年3月16日;提案者：A5
        - 我们假设A1、A2、A3收到A1的提案，A3、A4、A5收到A5的提案，而A3的回复将决定批准哪一个
        - 情况一
            - 假设A1的提案先送到A3处，而A5的侍从放假了，于是A3只收到A1的提案。 A1收到A3的回复后，就已经构成了一个多数派，于是提案通过称为决议
            - 可能过了很久A5的侍从上班后，A3才收到提案。由于决议已经通过，这个提案它就不再理会
        - 情况二
            - 假设A3先收到A1的提案，但是在决议成型前收到A5的提案。因为A5的提案比A1时间晚，则A3回复A5
                - 我已收到您的提案，等待最终批准，但是您之前有人提出将税率定为10%,请明察。
            - 于是，A1和A5都收到了回复，这时候关于税率就有两个提案在同时进行，但是A5知道之前已经有一个提案了，所以A1和A5都会广播
                - 税率已定为10%,新的提案不得再讨论本问题。
            - 这样就达成了共识。
            - 如果A5比A1的消息晚并且还是后到达的，那么A3则不进行理会。
    - 总结
        - 提案者发出提案后，会收到一些反馈，有两种结果，一种是自己的提案称为多数派，一种是没被接受，那就待会再试试
        - 如果称为多数派也不能认为这就是最终提案，因为这些接收者并不知道自己刚才同意的提案就是多数派
        - 所以，引入新的一轮确认提案，这就进入提交阶段
        - 提交阶段的提案发送出去，其他阶段进行提案值比较，返回最大的，然后确定最大值的提案为决议
- Multi-Paxos 算法
    - 如果leader是稳定的，那么可以直接指定，而避免了第一阶段多个提案的竞争
- Fast-Paxos 算法
    - Basic-Paxos 从客户端发起请求到请求结束，一个有三个消息延迟。而Fast-Paxos是两个，但是要求
        - 系统由3f+1个Acceptor 组成
        - 客户端要直接将请求发送到多个目标
    -