# 6 playbooks

- 文档
    - [blog](https://www.cnblogs.com/mauricewei/p/10053649.html)
    - [官方文档](http://www.ansible.com.cn/docs/playbooks.html)
- 通过配置文件的方式执行命令
- 格式示例

    ```yaml
    - hosts: aliyun
      name: Config Template
      vars:      # 变量
        http_port: 80
        https_port: 443
      remote_user: root   # 用户身份
      pre_tasks:
      - name: print task order
        debug:
          msg: 'pre_tasks 1'
      post_tasks:
      - name: print task order
        debug:
          msg: 'post_tasks 4'
      tasks:        # 定义任务
      - name: print task order
        debug:
          msg: 'tasks 3'
      - name: install nginx package
        apt: name=nginx state=present
        # remote_user: root  # 具体task的用户身份
        # sudo: no       # 是否使用sudo,不建议
    		# become: yes
    	  # become_user: root
    	  # become_method: sudo
      - name: write nginx config
        copy: content="# test head" dest=/etc/nginx/nginx.confg force=no
        notify:    # 事件触发
        - restart nginx
      - name: ensure nginx is running
        service: name=nginx state=started
      - name: echo string
        shell: echo "nginx is start, port {{ http_port }}"
      - include_tasks: test2.yaml  # 调用其他任务，会覆盖变量
        when: 
          - http_port==80 
          - https_port==443
      - import_tasks: test2.yaml  # 调用其他任务，不会覆盖变量
        when: http_port==81
      handlers:   # 被 notify 触发的任务
        - name: restart nginx
          service: name=nginx state=restarted
    # - hosts: other  其他play
    ```

- Roles
    - Roles负责组织playbooks，会自动的加载配置文件并进行分组
    - 文件结构

        ```yaml
        `-- roles
            `-- common
                |-- defaults
                |   `-- main.yaml
                |-- files
                |   `-- main.yaml
                |-- handlers
                |   `-- main.yaml
                |-- meta
                |   `-- main.yaml
                |-- tasks
                |   `-- main.yaml
                |-- templates
                |   `-- main.yaml
                `-- vars
                    `-- main.yaml
        ```

    - play指定roles

        ```yaml
        - hosts: webservers
          roles:
             - { role: common, tags: common }
        ```

- expect
    - 可以进行命令行的交互
    - 需要安装 pexpect
        - `pip install pexpect`    在安装ansible的环境中执行
    - 用法

        ```yaml
        - name: kube reset 
          expect: 
            echo: yes
            command: kubeadm reset
            responses:
              (?i)proceed: "y"  # 正则写法，包含preceed的选项
        			"reset proceed ": "y"  # 完全匹配的写法
            timeout: 30
        ```