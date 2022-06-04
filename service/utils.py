import json
import os
import string

# 用于构建倒排索引时，进行去除标点和数字等预处理操作
from datetime import datetime

import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from entity.global_entity import global_db

nltk.download("omw-1.4")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
wnl = WordNetLemmatizer()
porter_stemmer = PorterStemmer()

punc_dicts = {i: " " for i in string.punctuation}
num_dicts = {i: "" for i in "0123456789"}
punc_table = str.maketrans(punc_dicts)
num_table = str.maketrans(num_dicts)


def upload_news(path=""):
    if not path:
        path = os.path.dirname(__file__) + "/../entity/news.json"
    f = open(path, "r")
    news = json.load(f)

    path = os.path.dirname(__file__) + "/../entity/pred.txt"
    f = open(path, "r")
    cls = [line.strip() for line in f.readlines()]
    global_db.create_news_table()
    global_db.create_index_table()
    for i, doc in enumerate(news):
        global_db.insert_news(
            doc["title"], doc["time"], doc["content"], doc["source"], doc["url"], cls[i]
        )


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
            word = lemmatize_stem_word(str.lower(word))
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


# 转换为后缀波兰表达式
def transform_postfix(infix):
    i = 0
    infix = infix.replace(" ", "")
    stk = []
    postfix = []
    while i < len(infix):
        if infix[i] != "|" and infix[i] != "&" and infix[i] != "(" and infix[i] != ")":
            j = 0
            word = ""
            while (
                i < len(infix)
                and infix[i] != "|"
                and infix[i] != "&"
                and infix[i] != "("
                and infix[i] != ")"
            ):
                word += infix[i]
                i += 1
                j += 1
            postfix.append(word)
        elif infix[i] == "|" or infix[i] == "&" or infix[i] == "(":
            if infix[i] == "|":
                while stk and stk[-1] != "(":
                    postfix.append(stk[-1])
                    stk.pop()
            stk.append(infix[i])
            i += 1
        elif infix[i] == ")":
            while stk:
                if stk[-1] == "(":
                    stk.pop()
                    break
                postfix.append(stk[-1])
                stk.pop()
            i += 1
    while stk:
        postfix.append(stk[-1])
        stk.pop()

    return postfix


def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return None


def lemmatize_stem_word(word):
    pos = get_wordnet_pos(pos_tag([word])[0][1])
    if not pos:
        return word
    return porter_stemmer.stem(wnl.lemmatize(word, pos))


# 根据针对信息搜索
def search_by_specific_info(
    doc_ids,
    source=None,
    date_begin=None,
    date_end=None,
    interval=None,
    cls=None,
    order=False,
):
    if (not date_begin or not date_end) and interval:
        date_end = datetime.datetime.now()
        n, unit = interval.split()
        if unit == "week":
            date_begin = date_end - datetime.timedelta(weeks=int(n))
        elif unit == "day":
            date_begin = date_end - datetime.timedelta(days=int(n))
        elif unit == "month":
            date_begin = date_end - datetime.timedelta(days=30 * int(n))
    if not order:
        docs = global_db.query_specific(doc_ids, date_begin, date_end, source, cls)
    else:
        docs = []
        for i in doc_ids:
            res = global_db.query_specific([i], date_begin, date_end, source, cls)
            if res:
                docs += res
    return docs


def test_lemmatize_stem_word():
    lemmatize_stem_word("hello")
