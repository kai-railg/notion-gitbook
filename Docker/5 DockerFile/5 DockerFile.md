# 5 DockerFile

- 概述
    - 一般的，Dockerfile 分为四部分：基础镜像信息、维护者信息、镜像操作指令和容器启动时执行指令。
    - 每运行一条 RUN 指令，镜像添加新的一层，并提交。
    - CMD 指令，来指定运行容器时的操作命令。
    - 如果在同一个Dockerfile中创建多个镜像时，可以使用多个 FROM 指令（每个镜像一次）
- DockerFile
    - 语法规则备注
        - `{NAME:-tom}`  如果NAME 没有值，显示tom，否则显示值
        - `{NAME:+tom}`  如果NAME 有值，显示 tom，否则显示空
    - 示例

        ```docker
        # docs:  https://docs.docker.com/engine/reference/builder/

        FROM ubuntu
        # FROM [--platform=<platform>] <image> [AS <name>]
        # FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
        # FROM [--platform=<platform>] <image>[@<digest>] [AS <name>] # digest 哈希码

        ARG para=1
        # 用于在build时传递参数，可以设置默认值

        LABEL version="1.0" key="value"
        # LABEL <key>=<value> <key>=<value>   ...

        WORKDIR /app

        USER  root
        # USER <user>[:<group>] or USER <UID>[:<GID>]

        ADD test.txt /data
        # ADD test.* /data
        # ADD test.* data  # data=WORKDIR/data
        # ADD [--chown=<user>:<group>] <src>... <dest>
        # ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]

        COPY test.txt /data
        # COPY [--chown=<user>:<group>] <src>... <dest>
        # COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]

        ENV MY_NAME="kai" 
        # # LABEL <key>=<value> <key>=<value>  ...

        EXPOSE 80/tcp
        # EXPOSE 80 443

        VOLUME /data
        # 第一个路径为主机路径，第二个路径为容器路径
        # 匿名卷，不使用 : ，默认为 /data:/data
        # VOLUME /data:/data,/app:/app
        # VOLUME [ "/data" ]

        RUN apt-get install -y curl
        # RUN ["/bin/sh", "-c", "echo 1"]

        CMD ["/usr/bin/wc","--help"]
        # 同 RUN

        ENTRYPOINT ["/bin/sh", "-c", "echo 1"]
        # 同 RUN

        ONBUILD RUN echo "next build"
        # 该镜像作为基础镜像构建时会触发执行

        STOPSIGNAL 9
        # 内核系统调用表的信号，或格式化的信号名称，如SIGKILL

        HEALTHCHECK NONE
        # HEALTHCHECK --interval=5m --timeout=3s \ CMD curl -f http://localhost/ || exit 1
        # NONE 禁用基础镜像的健康检查

        SHELL [ "/bin/sh", "-c" ]
        ```

    - `ARG`
        - `From` 指令支持由第一个 `FROM` 之前的任何 ARG 指令声明的变量
        - 不建议使用，如果arg的值与前一版本不同，会导致缓存丢失。
        - 作用域为单个的FROM，如果声明在FROM内
        - 使用 `docker build --build-arg <name>=key` 声明变量
        - 在 FROM 之前声明的 ARG 不在构建阶段之内，因此不能在 FROM 之后的任何指令中使用它。
        - 若要使用在第一个 FROM 之前声明的 ARG 的默认值，请在构建阶段中使用没有值的 ARG 指令

        ```bash
        ARG VERSION=latest
        FROM busybox:$VERSION
        ARG VERSION
        RUN echo $VERSION > image_version
        ```

        - docker预定义的ARGs
            - `HTTP_PROXY`
            - `http_proxy`
            - `HTTPS_PROXY`
            - `https_proxy`
            - `FTP_PROXY`
            - `ftp_proxy`
            - `NO_PROXY`
            - `no_proxy`
    - `FROM`
        - 第一条指令必须为 FROM 指令，用于为映像文件构建过程指定基准镜像，后续的指令运行于此基准镜像所提供的运行环境
        - `docker build` 时会在 docker 主机 → 镜像仓库 查找并拉取指定的镜像文件，不存在时会返回一个错误信息
        - `FROM <repository>[:<tag>]` 或者 `FROM <repository>@<digest>`
            - <`repository`> 为基准镜像，<`tag`> 为标签，省略是默认为`latest`，<`digest`> hash码
        - 关于版本：
            - Alpine，面向安全应用的轻量级Linux发行版，包管理工具apk
            - Stretch，Debian GNU/Linux 9版本的代号
            - Buster，Debian GNU/Linux 10版本的代号
            - Slim，    仅包含运行 Java 所需的最小包
    - `ENV`
        - 设置环境变量，一句一层，适用于所有的DockerFile
        - `ENV x y`   只能设置一个值，空格使用转义符
        - `ENV x=y s=z d=c`  可以一次设置多个值 ，推荐使用
        - 可以使用 `docker run --env` 更改环境变量的值
    - `WORKDIR`
        - 为 `RUN、 CMD、ENTRYPOINT、COPY` 和 `ADD` 指令设置工作目录。 如果 `WORKDIR` 不存在，即使它不在任何后续的 Dockerfile 指令中使用，它也会被创建
        - 可以多次使用 `WORKDIR`

            ```bash
            WORKDIR /a
            WORKDIR b
            WORKDIR c
            RUN pwd      # output为 /a/b/c
            ```

    - `COPY`
        - `COPY <src>... <dest>`
        - `COPY ["<src>",... "<dest>"]` 对于包含空格的文件或目录名是必要的
        - Copy 指令从 src 复制新文件或目录，并添加到位于 dest 路径的容器的文件系统中。
        - 同 `ADD` 相似
        - 需要将文件提前复制到`Dockerfile`所在目录
    - `ADD`
        - 格式为 `ADD <src> <dest>`
        - 该命令将复制指定的 `<src>` 到容器中的 `<dest>`，支持正则，支持go语法
        - 其中 `<src>` 可以是url（自动下载但不解压） 或可识别的压缩包（自动解压）
            - 如果要下载的url需要身份验证，请使用 RUN wget 配合其他工具
        - 创建的所有新文件和目录的 UID 和 GID 为0。
        - 如果 src 是一个 URL
            - 如果 dest 没有以斜杠结尾，那么文件将从 URL 下载并复制到 dest。
            - 如果 dest 以一个尾部斜杠结尾，那么文件下载到 `dest/filename`
        - 如果 src 是一个目录，仅复制内容，不复制目录本身
        - 如果 dest 不存在，则创建。
    - `USER`
        - 指定运行容器时的用户，包括后续的`RUN、CMD、ENTRYPOINT`
        - `USER <user>[:<group>]`
        - `USER <UID>[:<GID>]`
    - `EXPOSE`
        - Expose 指令通知 Docker 容器在运行时监听指定的网络端口
        - 可以指定协议，默认Tcp。比如`80/tcp`或`80`表示开放80端口的tcp协议
        - Expose 指令实际上并不发布端口，只是起到文档的作用。
        - 要在运行容器时发布端口，使用-p 标志发布所有公开的端口并将它们映射到高级端口
        - 
    - `RUN`
        - 格式为 `RUN <command>` 或 `RUN ["executable", "param1", "param2"]`
        - 默认即前者使用`/bin/sh -c`
        - 后者使用`exec`，也可以写作`RUN ["/bin/bash", "-c", "echo hello"]`
            - 必须使用双引号
        - 对于交互式的命令，`RUN`后面跟着 `DEBIAN_FRONTEND=noninteractive`
    - `CMD`
        - `CMD ["executable","param1","param2"]` 使用 `exec` 执行，推荐方式；
        - `CMD command param1 param2` 在 `/bin/sh` 中执行，提供给需要交互的应用；
        - `CMD ["param1","param2"]` 提供给 `ENTRYPOINT` 的缺省参数；
        - 只有最后一条CMD命令生效
        - Cmd 的主要目的是为正在执行的容器提供缺省值
        - Run 实际上运行一个命令并提交结果; CMD 在构建时不执行任何内容，但是为映像指定预期的命令。
    - `LABEL`
        - Label 指令将元数据添加到映像中。 Label 是键值对，可以覆盖
        - 一个 Label 为一层
        - 格式示例，通过 `docker insepect` 可以查看

            ```bash
            LABEL multi.label1="value1" multi.label2="value2" other="value3"
            ```

    - `ENTRYPOINT`
        - Entrypoint 允许您配置将作为可执行文件运行的容器，两种形式：
        - `ENTRYPOINT ["executable", "param1", "param2"]` 推荐
        - `ENTRYPOINT command param1 param2`（shell执行，会阻止使用任何cmd和run参数）
        - 此命令不会被 `docker run` 时的参数所覆盖，且会被当作参数补到指令的末尾。
        - 如果需要覆盖 `ENTRYPOINT` 指令，需要 `docker run -- entrypoint "str"`
        - 只有 Dockerfile 中的最后一条 ENTRYPOINT 指令才会生效
        - Exec 形式的 `ENTRYPOINT`
            - 使用 `ENTRYPOINT` 的 exec 形式来设置相当稳定的默认命令和参数，然后使用任何一种 CMD 形式来设置更可能更改的其他默认值。

            ```bash
            FROM ubuntu
            ENTRYPOINT ["top", "-b"]
            CMD ["-c"]
            ```

    - `VOLUME`
        - Volume 指令创建具有指定名称的挂载点
        - `VOLUME ["/data"]`
        - `VOLUME /myvol`
    - `ONBUILD`
        - 向镜像添加一个触发器，在以后将该映像用作另一个构建的基础时执行
        - `ONBUILD [INSTRUCTION]` ，比如 `ONBUILD ADD . /app/src`
    - `MAINTAINER <name>`  维护者信息，已弃用，请使用Label
- docker build
    - 编写完成 Dockerfile 之后，可以通过 `docker build` 命令来创建镜像。
    - 基本的格式为 `docker build [选项] 路径`，该命令将读取指定路径下（包括子目录）的 Dockerfile，并将该路径下所有内容发送给 Docker 服务端，由服务端来创建镜像。因此一般建议放置 Dockerfile 的目录为空目录。也可以通过 `.dockerignore` 文件（每一行添加一条匹配模式）来让 Docker 忽略路径下的目录和文件。
    - 要指定镜像的标签信息，可以通过 `-t` 选项，例如
        - `$ sudo docker build -t myrepo/myapp /tmp/test1/`