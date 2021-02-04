# 5 Filebeat

- 配置文件, `filebeat.yml`

    ```jsx
    filebeat.inputs:
    - type: log
      paths:
        - /Users/railg/Desktop/packages/Project/elasticsearch/logs/elasticsearch.log
    # logstash 需要配置input
    output.logstash:
      hosts: ["localhost:5044"]
    ```

- logstash配置

    ```jsx
    input {
      beats {
        port => "5044"
      }
    }
    ouput {}
    ```

- 启动
    - `./filebeat -e -c filebeat.yml -d "publish"`
- 删除注册表，从头读取文件
    - `rm data/registry`