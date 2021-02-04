# 2 ES的CURD

- _cat
    - `/_cat/nodes`  查看节点
    - `/_cat/plugins`  查看插件
    - `/_cat/indices`  查看索引

- create
    - 如果 ID 已经存在,会失败
    - 支持自动生成文档 ID 和 指定文档 ID
    - `POST _index/_doc/id {}`
    - `PUT _index/_doc/id?op_type=create {}`
    - 
- index
    - 如果ID 已经存在,会先删除已有的文档.然后再创建,版本号会增加
    - `PUT _index/_doc/id {}`
- Update
    - 文档必须存在
    - `POST _index/_update/id {"doc":{}}`
- Delete
    - `delete  _cat/_all` 删除全部
- bulk
    - 在一次API调用中，支持对不同索引进行操作
    - 操作中单条操作失败，不会影响其他操作

    ```json
    POST _bulk
    {"index": {"_index": "test", "_id":1}}
    {"field": "value1"}
    {"update": {"_index": "test", "_id":1}}
    {"doc":{"field2":"value2"}}
    {"create": {"_index": "test2", "_id":1}}
    {"field": "value1"}
    {"delete": {"_index":"test2","_id":1}}
    ```

- mget
    - 一次性读取多个文档

    ```json
    GET _mget
    {
      "docs":[
        {
          "_index": "test",
          "_id": 1
        },
          {
          "_index": "test2",
          "_id": 1
        }
      ]
    }
    ```

- msearch
    - 批量查询

    ![2%20ES%E7%9A%84CURD%20c2ccc9449aab40f697887b51cdc0e001/Untitled.png](2%20ES%E7%9A%84CURD%20c2ccc9449aab40f697887b51cdc0e001/Untitled.png)