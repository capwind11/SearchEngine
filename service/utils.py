import json
import os
import string

# 用于构建倒排索引时，进行去除标点和数字等预处理操作
from entity.global_entity import global_db

punc_dicts = {i: " " for i in string.punctuation}
num_dicts = {i: "" for i in "0123456789"}
punc_table = str.maketrans(punc_dicts)
num_table = str.maketrans(num_dicts)


# 从sql中加载新闻保存到本地json
def download_news(path=""):
    if not path:
        path = os.path.dirname(__file__) + "/../entity/news.json"
    docs = global_db.query_all_docs()
    f = open(path, "w", newline="\n")
    f.write("[")
    for i, doc in enumerate(docs):
        json.dump(
            {
                "id": doc[0],
                "title": doc[1],
                "content": doc[2],
                "source": doc[3],
                "time": doc[4],
                "url": doc[5],
                "cls": doc[6],
            },
            f,
            indent=2,
        )
        if i < len(docs) - 1:
            f.write(",\n")
    f.write("]")
    f.close()


# 构建倒排索引
def build_inverted_index(path=""):
    if not path:
        path = os.path.dirname(__file__) + "/../entity/news.json"
    f = open(path, "r")
    news = json.load(f)
    indexes = {}
    for i, item in enumerate(news):
        content = item["content"].translate(punc_table)
        content = content.translate(num_table)
        title = item["title"].translate(punc_table)
        title = title.translate(num_table)
        for word in set(content.split() + title.split()):
            if word not in indexes:
                indexes[word] = []
            indexes[word].append(item["id"])
    del news
    indexes = sorted(indexes.items(), key=lambda x: x[0])
    inverted_index = {}
    for k, v in indexes:
        inverted_index[k] = v
    del indexes
    with open(os.path.dirname(__file__) + "/../entity/inverted_index.json", "w") as f:
        json.dump(inverted_index, f, indent=1)
    index = []
    for k, v in inverted_index.items():
        index.append((k, ",".join([str(i) for i in v])))
    global_db.insert_inverted_index(index)
    del inverted_index


# 加载倒排索引
def load_inverted_index(path=""):
    if not path:
        path = os.path.dirname(__file__) + "/../entity/inverted_index.json"
    with open(path, "r") as f:
        index = json.load(f)
    return index
