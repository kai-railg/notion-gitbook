# 6 Mapping

- Mapping 类似数据库中的schema的定义，作用如下：
    - 定义索引中字段的名称
    - 定义字段的数据类型
    - 字段。倒排索引的相关设置（比如这个字段不被索引）
- Mapping会把JSON文档映射成Lucene需要的扁平格式
- 一个Mapping属于一个索引的Type
    - 每个文档都属于一个Type
    - 一个Type有一个Mapping定义
- `Mapping的字段类型`
- Dynamic Mapping
    - 写入文档时，如果索引不存在，会自动创建索引
    - 无需手动定义 Mappings，es 会根据文档信息推算字段的类型
    - 推断有可能不准确，对该类型最好手动定义
    - 更改Dynamic Mapping的类型
        - 分为新增字段和已有字段两种情况
        - 新增字段
            - Dynamic 设置为`True`，Mapping会随着新增文档而更新
            - Dynamic 设置为`False`，Mapping 不会被更新，新增字段也无法被索引，但是会出现在 _source 中
            - Dynamic 设置为`Strict`，拒绝文档写入

        - 已有字段
            - 不支持修改文档定义，Lucene实现的倒排索引一旦生成，就无法修改
                - 如果修改了字段的数据类型，会导致已索引的数据无法被搜索
                - 如果希望改变字段类型，就比如 Reindex API
    - 控制 Dynamic

        ```json
        PUT test/_mapping
        {
          "dynamic": "true"
        }
        ```

        ![6%20Mapping%209a8c748194e64770adf8c39ae5fda6b9/Untitled.png](6%20Mapping%209a8c748194e64770adf8c39ae5fda6b9/Untitled.png)

- 显示定义Mapping
    - 语法

        ```json
        PUT test
        {
          "mappings" : {
            "dynamic" : "true",
            "properties" : {
              "field" : {
                "type" : "text",
                "index": true,   // 是否被索引
        				"null_value": "NULL", 
        				"copy_to": "fullname",
        				"index_options": "docs", //
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              }
            }
          }
        }
        ```

        - `index_options`
            - docs  记录doc id
            - freqs  记录doc id 和term frequencies
            - postions 记录 doc id  和term frequencies 和 term postion
            - offsets 记录 doc id  和term frequencies 和 term postion 和 character offects
        - `null_value`
            - 需要对null值进行搜索
            - 只有type:"keyword" 才支持null_value
        - `copy_to`
            - 将字段的值copy到目标字段，可以对目标字段进行搜索
            - copy_to的目标字段不会出现在_source中
    - 基本的流程
        - 可以先创建一个index，获取其动态mapping定义
        - 修改后，使用其定义创建你的索引
    - 

- 多字段类型
    - 厂商名字实现精确匹配
        - 增加一个keyword字段
    - 使用不同的analyzer
- Index Template
    - 索引模版，预设定Mappings 和 Settings，并按照一定的规则，自动匹配到新创建的索引上。
        - 模版仅在一个索引被新创建时，才会产生作用。
        - 可以设定多个Index Template，这些设置会自动Merge到一起
        - 可以指定order的数值，控制merge的过程
    - Template

        ```json
        PUT _template/template_default
        {
          "index_patterns": ["test*"], // 以test开头的suo
          "order": 0,  // 权重
          "version": 1, //
          "settings": {
            "number_of_replicas": 1,
            "number_of_shards": 1
          }
        }
        ```

        - 当一个索引被创建时
            - 应用ES默认的Settings和Mappings
            - 应用order数值低的Index Template中的设定
            - 应用order数值高的Index Template中的设定，之前的设定会被覆盖
            - 应用创建索引时用户所指定的Settings和Mappings，并覆盖之前模版中的设定
- Dynamic Template
    - 根据ES识别的数据类型，结合字段名称，来动态设定字段类型
        - 定义在某个index的mappings中
        - Template有一个名称
        - 匹配规则是一个数组
        - 为匹配的字段设置Mapping
    - 语法

        ```json
        PUT test
        {
          "mappings": {
            "dynamic_templates":[
              {
                "full_name":{
                  "path_match": "name*",
                  "path_unmatch": "*.middle",
                  "mapping":{
                    "type": "text",
                    "copy_to": "full_name"
                  }
                }
              }
              ]
          }
        }
        ```