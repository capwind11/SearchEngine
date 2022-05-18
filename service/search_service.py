# 构建倒排索引

from entity.global_entity import *


# 目前只实现了and功能
def boolean_search(words):
    if len(words) == 0:
        return set()
    doc_ids = global_db.query_doc_ids_by_word(words[0])
    for word in words[1:]:
        doc_ids = doc_ids.intersection(global_db.query_doc_ids_by_word(word))
    docs = global_db.query_by_doc_id(doc_ids)
    return docs


# 实现根据来源source和日期进行查找
def specific_search(news_date, source):
    return global_db.query_by_specific_info(news_date, source)


def test_boolean_and():
    print(boolean_search(["recovery", "from", "COVID", "Wuhan", "January"]))
