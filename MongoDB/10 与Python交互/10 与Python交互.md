# 10 与Python交互

- 1 安装包

    pip install pymongo

- 2 import

    import pymongo

- 3 连接，创建客户端

    client=pymongo.MongoClient("localhost", 27017)

    账号验证： client['admin'].authtication(user,pwd)

    client=pymongo.MongoClient("mongodb://user:pwd@127.0.0.1:27017")

- 4 获得数据库

    db=client.test1

- 5 获得集合

    stu = db.stu

- 6 官方文档链接

    [http://api.mongodb.com/python/current/](http://api.mongodb.com/python/current/)