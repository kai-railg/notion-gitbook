# 4 volume

- 1 由docker 管理的卷
    - `docker run -it -v /data —name b2 busybox`

    通过 docker inspect b2 查看 Mounts 下的 Source 的值，就是卷的目录。对此目录下的任意文件操作，都可以在 b2 容器中呈现，同理，在b2 容器中 对 data 目录的修改也可以在主机的目录下查看。

- 2 挂载的卷

    `docker run --name b2 -it -v /data/b2:/data --rm busybox`

    这样就有了脱离容器生命周期的持久化文件

- 3 复制已存在的卷

    `docker run --name b3 -it -v —volumes-from b2 --rm busybox`