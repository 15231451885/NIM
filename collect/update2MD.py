import json
from pymongo import MongoClient

# 连接 MongoDB 数据库
client = MongoClient('mongodb://localhost:27017/')
# 选择要使用的数据库
db = client['NIM']
# 选择要使用的集合
collection = db['domain2ip']

# 打开 JSON 文件并读取数据
file_path=r"/home/wzy/PycharmProjects/pythonProject/NIM/collect"# 获取文件路径
fileR = file_path + r'/domain2ip.json'
with open(fileR, 'r') as file:
    for line in file:
        data=json.loads(line)
        # 将数据插入到 MongoDB 数据库中
        existing_doc = collection.find_one({"domain": data["domain"]})

        if existing_doc:
            # 如果存在相同域名的文档，更新该文档的 date 列表
            existing_date = existing_doc["date"]
            existing_date.extend(data["date"])
            collection.update_one({"domain": data["domain"]}, {"$set": {"date": existing_date}})
        else:
            # 如果不存在相同域名的文档，插入新的文档
            collection.insert_one(data)

# 关闭 MongoDB 连接
client.close()


