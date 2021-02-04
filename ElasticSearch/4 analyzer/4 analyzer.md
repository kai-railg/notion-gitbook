# 4 analyzer

- 分词器是专门处理分词的组件，analyzer由三部分组成
    - Character Filters  针对原始文本处理，比如去除html
    - Tokenizer 按照规则切分单词
    - Token Filter 将切分的单词进行加工、小写、删除stopwords、增加同义词
- 默认分词器会按词切分，转小写处理，不启用停用词
- 查看分词情况
    - `GET _analyze {"analyzer": "standard", "text": "test word"}`
- analysis-icu 分词器，更好的支持亚洲语言的Unicode
    - `POST _analyze {"analyzer": "icu_analyzer", "text": "这个苹果不大好吃"}`
- 其他中文分词器
    - IK
    - THULAC
- 精确词和全文本的区别
    - 精确词
        - 包括数字、日期、特定的字符串（比如BeiJing）
        - ES的`keyword`类型
        - 不需要被分词
    - 全文本
        - 非结构化的文本数据
        - ES的`text`类型
        - 需要被分词
- 自定义分词
    - 当ES自带的分词器无法满足需求时，可以自定义分词器。通过自组合不同的组件来实现