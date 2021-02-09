# 1 docker 基础

- 流程图

    ![1%20docker%20%E5%9F%BA%E7%A1%80%20c25e430129d74e29b476379fd563fb85/docker.png](1%20docker%20%E5%9F%BA%E7%A1%80%20c25e430129d74e29b476379fd563fb85/docker.png)

    ![1%20docker%20%E5%9F%BA%E7%A1%80%20c25e430129d74e29b476379fd563fb85/docker%201.png](1%20docker%20%E5%9F%BA%E7%A1%80%20c25e430129d74e29b476379fd563fb85/docker%201.png)

- 常用命令
    - `docker info`  docker的基本信息
    - `docker search x`   搜索镜像
    - `docker pull x`       拉取镜像
    - `docker images` `docker image ls` 本地镜像
    - `docker rmi x` `docker image rm x`  删除镜像
        - `-f` 强制删除
    - `docker tag 26865d03b2ef user/ht:v0.1`  打上标签
    - `docker tag 26865d03b2ef user/ht:v0.1 user/ht:latest`  设置多个标签
        - 多个标签都是引用同一个镜像，删除镜像时先删除镜像名称，最后镜像ID
        - 标签会覆盖已有的

    - `docker ps`   查看运行状态容器
    - `docker ps -a`  查看所有容器
    - `docker inspect x`  查看容器详细信息
        - `docker inspect -f {{.Mounts}} x`
            - 可以使用 go语言过滤查找， 子目录下通过 `.` 查找
    - `docker run —-name x -it -d --rm image`  运行容器
        - `-it` 交互
            - `docker exec -it x /bin/sh`  可以进入容器环境中
        - `-d` 后台
        - `-p 80:80` 将指定的容器端口映射到宿主机指定的动态端口
            - `iptables -t nat -vnL`  查看主机端口映射

            docker run —name x -p 主机名:8080:80  镜像  ，将指定容器端口映射到宿主机的指定端口

            docker run —name x -p 80:80  镜像  ，将指定的容器端口映射到宿主机指定的动态端口

            docker run —name x -p 主机名::80  镜像  ，将容器端口映射到宿主机的指定端口

            docker run —name x -p 80  镜像  ，指定容器端口映射到宿主机的一个动态端口

            docker run —name x —network container:x1 镜像，  联盟式接口启动容器，共享ip地址

            docker run —name x —network host 镜像，  直接使用宿主机端口 

        - `-d` 后台
        - `—-rm` 终止后删除
        - `-v /data/b2:/data`  存储卷，挂载宿主机目录
        - `-v —volumes-from`   挂载已有的存储卷
    - `docker exec -it x /bin/sh`   交互式环境
        - `exit`  输入后退出
    - `docker kill x` 终止容器
        - 相当于kill -9， stop 相当于 kill -15
    - `docker rm x` 删除容器
    - `docker port x`   查看容器映射的端口
    - `docker logs x`   查看容器日志

- Docker的本质
    - 容器是一种特殊的进程。
    - Docker技术的核心：`隔离`和`限制`。
        - 在Linux 创建新进程的时候添加`一系列参数`，通过`Cgroups` 技术来制造限制，通过`Namespace` 技术用来实现隔离。
        - Linux 提供了 `Mount`、`UTS`、`IPC`、`NetWork`、`User`、`PID` 六种 Namespace
    - Namespace 技术对进程的视线做了隔离，只能让其看到指定的内容。对于宿主机而言，进程之间并没有什么区别。
        - 在容器中执行ps，会看到两个进程

            ```docker
            / # ps
            PID USER TIME COMMAND 
            1 root 0:00   /bin/sh    # 与容器交互的指令，在外部执行的/bin/sh
            10 root 0:00  ps         # 容器中执行的指令
            ```

        - 本来，当我们在宿主机运行一个/bin/sh程序，操作系统都会给它分配一个PID，比如100。
        - 而我们通过Docker运行一个/bin/sh程序，Docker会让这个程序永远看不到前面99个的程序，误以为自己就是PID为1的进程。
        - 所以，宿主机上的100号进程，其实就是容器中的1号进程。
        - 这种技术就是`Namespace`。
        - Linux在创建进程的时候用的clone命令，而Docker做的就是在clone的时候加上各种各样的Namespace参数，所以本质上启动的依然是宿主机的进程。
    - 敏捷和高性能是容器最大的优点，但是主要的问题是隔离的不彻底
        - 因为容器技术本质上是一个应用进程，Docker对宿主机额外的资源占用几乎没有
        - 但是多个容器之间用的是同一个宿主机的操作系统内核。
        - Linux内核中，有些资源和对象是不能被Namespace化的，比如时间
    - Linux Cgroups (Linux Control Group) 是用来为进程设置资源限制的重要功能。
        - 容器里的进程与宿主机上的进程依然是平等竞争关系，这个进程可能会把资源吃光
        - Cgroups 限制了一个进程组能够使用的资源上限，包括CPU、内存、磁盘、网络等
    - Mount Namespace特殊的地方在于，它对容器视图的改变，一定是伴随着挂载操作才能生效
        - 如果直接clone进程，容器里看到的目录和宿主机是完全一样的
        - Mount Namespace 修改的是，容器对挂载点的认知
            - 挂载操作发生后，进程的视图才会改变
            - 而在此之前，新创建的容器会`直接继承宿主机的文件系统`
        - 容器中是以 tmpfs 的方式单独挂载的，因为挂载发生在容器中，所以挂载对宿主机不可见
        - Linux 中 `chroot` 命令可以完成一个独立的文件系统的隔离环境，而`不是继承宿主机的文件系统`
            - chroot， 改变进程的根目录到你指定的位置
        - 而 Mount Namespace 是对 chroot 的不断改良，为了让容器的根目录看起来更真实，一般会在容器的根目录下挂载一个完整操作系统的文件系统
        - 在这个挂载在根目录上、用来为容器进程提供隔离后执行环境的文件系统，就是所谓的`容器镜像`。专业名称叫 `rootfs` (根文件系统)。
    - 容器镜像
        - rootfs 是一个操作系统所包含的文件、配置和目录，不包括内核。
        - rootfs 实现了容器的重要特性：`一致性`
            - 镜像打包了应用程序所需要的完整的执行环境
            - 为了不重复制作rootfs，Docker引入了层的概念。
        - Docker 的rootfs 引入了层 (layer) 的概念。用户制作镜像的每一步操作，都会生成一个层，也就是一个增量的rootfs。其基于`联合文件系统 (Union File System)` 实现。
            - UnionFS 主要是将多个不同位置的目录联合挂载到一个目录下
                - 相同的文件会被合并
            - Docker 现在的用的是 `AuFS`，基于 UnionFS的改进
            - rootfs 由三部分组成
                - 可读写层
                    - 修改容器产生的内容会以增量的形式在这里
                    - 如果是delete操作，比如删除foo文件，会产生一个.foo文件，联合挂载后原foo文件就会被遮挡从而不可见
                - init 层
                    - 存放配置文件的信息，commit 命令不包含该层
                - 只读层
                    - 操作系统的文件
    - Docker Volume，允许你将宿主机上指定的目录或者文件，挂载到容器里面进行读取和修改操作
        - 两种方式挂载
            - `docker run -v /test ...`
                - 在宿主机上创建临时目录 `/var/lib/docker/volumes/[VOLUME_ID]/_data` 挂载到容器的/test目录
            - docker run -v /home:/test ...
                - 挂载宿主机上的/home目录到容器中的/test目录
        - 在rootfs准备好之后，执行chroot之前，把Volume指定的宿主机目录，挂载到指定的容器目录中去，Volume的挂载工作就完成了
        - 执行挂载操作时，Mount Namespace已经开启了。所以，挂载事件只在容器里可见，宿主机上也是看不见这个挂载点的
        - 主要靠`挂载绑定`技术实现。
            - 允许你将一个目录或文件，而不是整个设备，挂载在到一个指定的目录
            - 绑定挂载实际上是一个inode替换的过程
                - inode可以理解为存放文件内容的对象
                - dentry是访问这个inode的指针
                - 可以理解为将容器挂载目录的dentry指向宿主机被挂载目录的inode
            - 而 docker commit 时会忽略容器挂载目录的内容，因为docker commit 作用在宿主机上，而宿主机对目录是无感的
    - 容器核心原理
        1. 启用 Linux Namespace 配置
        2. 设置指定的 Cgroups 参数
        3. 切换系统的根目录
            - chroot
    - 一个进程，可以进入到另一个进程的Namespace中，这就是docker exec 的实现原理。