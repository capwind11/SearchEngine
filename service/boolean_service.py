# 构建倒排索引

from entity.global_entity import *

# 目前只实现了and功能
from service.utils import (
    transform_postfix,
    search_by_specific_info,
    lemmatize_stem_word,
)


# boolean搜索
def boolean_search(
    keywords, source=None, date_begin=None, date_end=None, interval=None, cls=None
):
    if len(keywords) == 0:
        return None
    postfix = transform_postfix(keywords)

    stk = []
    all_doc_ids = global_db.query_doc_ids()
    for elem in postfix:
        if elem != "|" and elem != "&":
            if elem[0] == "-":
                word = lemmatize_stem_word(str.lower(elem[1:]))
                stk.append(
                    all_doc_ids.difference(global_db.query_doc_ids_by_word(word))
                )
            else:
                word = lemmatize_stem_word(str.lower(elem))
                stk.append(global_db.query_doc_ids_by_word(word))
        elif elem == "|":
            tmp = stk[-1].union(stk[-2])
            stk.pop()
            stk.pop()
            stk.append(tmp)
        else:
            tmp = stk[-1].intersection(stk[-2])
            stk.pop()
            stk.pop()
            stk.append(tmp)
    doc_ids = stk[-1]
    return search_by_specific_info(doc_ids, source, date_begin, date_end, interval, cls)
