# MySQL字符串索引的设计+字典树

- 全字段使用索引
    - 占用空间更大
    - 判断一行符合条件后继续扫描直到不符合条件的为止，回表次数取决于满足条件的行数
    - 可以利用覆盖索引
- 前缀索引
    - 占用空间更少
    - 判断一行满足条件后，进行回表查询判断全字段是否符合条件
    - 回表次数取决于满足条件的前缀索引的总行数
    - 不可以利用覆盖索引
- 倒序索引
    - 和全字段所索引类似，倒序是为了提高区分度
- hash
    - 提高区分度，减少索引长度，
    - 但是需要额外建立索引，hash值可能会冲突
- 利用Trie树实现字符串索引
    - 取决于应用场景，比如字符串有区间范围、字符串部分相同、字符串的更新频率
    - 可以剪枝，减少磁盘占用过大
        - 比如学校学生的身份证号，年龄可以取一个范围
    - 子节点可以合并，减少树高
        - 比如一个地区的学生，身份证前缀相同
    - 缩点优化，尽可能的利用缓存
        - 学生入学后统计的身份证信息变动较少
    - 代码

        ```jsx
        class TrieNode:
            def __init__(self):
                self.nodes = dict()  # 构建字典
                self.primary_id = 0  # 主键ID

            def insert(self, word: str, primary_id):
                curr = self
                for char in word:
                    if char not in curr.nodes:
                        curr.nodes[char] = TrieNode()
                    curr = curr.nodes[char]
                curr.primary_id = primary_id

            def insert_many(self, words: [str]):
                for word, primary_id in words:
                    self.insert(word, primary_id)

            def search(self, word: str):
                """
                返回0表示不存在，数据先插入到数据库，再在字典树中插入主键ID
                """
                curr = self
                for char in word:
                    if char not in curr.nodes:
                        return False
                    curr = curr.nodes[char]
                return curr.primary_id
        ```