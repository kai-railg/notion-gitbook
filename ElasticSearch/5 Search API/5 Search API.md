# 5 Search API

- `/_search`  查询所有索引
- `/index1/_search`  index1索引
- `/index1,index2/_search`  index1和index2索引
- `/index*/_search`  index开头的索引
- URI Search
    - 使用URL携带参数进行查询
    - URI查询
        - 使用q指定查询的字符串
        - `[http://localhost:9200/index_name/_search?q=title:小明&df=tile&sort=field:desc,id:asc&from=100&timeout=3&size=100](http://localhost:9200/index_name/_search?q=title:小明&df=tile&sort=field:desc,id:asc&from=100&size=100)`  `{"profile": "true"}`
        - df查询可以简写为
            - `?q=title:name`
        - df 默认字段，不指定时会对所有字段进行查询
        - sort，from，size | 排序，分页（偏移和每页数据）
        - timeout  查询最大时间
        - [`相关文档`](https://www.cnblogs.com/daynote/p/11076965.html)
    - URI查询的几种方式
        - Term、Phrase、Bool 查询
        - `/index/_search?q=title:"A B"`
            - “A B” 等效于 A AND B，`Phrase Query` 必须同时出现并要求顺序保持一致
        - `/index/_search?q=title:A B`
            - A B 等效于 title:A 和 全字段:B， `TermQuery` + 泛查询
        - `/index/_search?q=title:(A B)`
            - (A B) 等效于 A OR B，`BooleanQuery`
    - bool查询
        - 布尔查询默认为OR
        - NOT、AND、OR  或者 !  &&  ||
        - `/index/_search?q=title:(A AND B)`
        - +(%2B) 、-
        - `/index/_search?q=title:(A %2B B)`
    - 范围查询
        - >、<、≥、≤
        - [] 开区间、{} 闭区间 ，[* TO 2019}
        - `/index/_search?q=year:[* TO 2019}`
        - `/index/_search?q=year:(>2010 && ≤2018)`
    - 通配符和正则
        - `?`  1个占位符
            - `title:mi?d`
        - `*`  0或多个占位符
            - `title:be*`
        - []
            - `title:[bt]oy`
    - 模糊匹配与近似查询
        - `title:toda~1`    模糊匹配一个符号
        - `title:"today is"~2` ， 中间可以间隔两个单词

- Request Body Search
    - 使用JSON，DSL（Domain Specify Langrage）
    - _source filter
        - `{"_source": ['name*']}`  结果只返回指定的，支持通配符
    - script_fields
        - 可以进行返回结果的处理

        ```json
        GET test/_search
        {
          "script_fields": {
            "new_field": {
              "script": {
                "lang": "painless", 
                "source": "doc['field1'].value+'hello'"
              }
            }
          },
          "query": {
            "match_all": {}
          }
        }
        ```

    - match query
        - match

            ```json
            GET test/_search
            {
              "query": {
                "match": {
                  "field": {
                    "query": "val1 val2",
                    "operator": "and"
                  }
                }
              }
            	}
            ```

        - match Pharse
            - 查询内容按顺序进行查找

            ```json
            GET test/_search
            {
              "query": {
                "match_phrase": {
                  "field": {
                    "query": "val1 val2",
                    "slop": 1 # 代表中间可以间隔一个单词
                  }
                }
              }
            	}
            ```

    - query string
        - 查询单个或多个字段

            ```json
            GET test/_search
            {
              "query": {
                "query_string": {
                  "fields": ["field", "field2"], // 多个字段
            			// "default_field": "field",   // df 单个字段
                  "query": "value1 AND value2"
                }
              }
            }
            ```