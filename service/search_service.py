# 构建倒排索引
import datetime

from entity.global_entity import *

# 目前只实现了and功能
from service.utils import transform_postfix


# boolean搜索
def boolean_search(statement):
    if len(statement) == 0:
        return set()
    postfix = transform_postfix(statement)
    stk = []
    for elem in postfix:
        if elem != "|" and elem != "&":
            stk.append(set(global_db.query_doc_ids_by_word(elem)))
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
    docs = global_db.query_by_doc_id(doc_ids)
    return docs


# 距离今天interval时间段内的新闻
def specific_search_by_date_interval(interval, source=""):
    now = datetime.datetime.now()
    n, unit = interval.split()
    if unit == "week":
        previous_date = now - datetime.timedelta(weeks=int(n))
    elif unit == "day":
        previous_date = now - datetime.timedelta(days=int(n))
    elif unit == "month":
        previous_date = now - datetime.timedelta(days=30 * int(n))
    return global_db.query_by_specific_info(previous_date, now, source)


# 根据日期区间查找，从date1到date2的所有新闻
def specific_search_by_period(date1, date2, source=""):
    return global_db.query_by_specific_info(date1, date2, source)


def test_boolean_and():
    print(boolean_search("senior&official|test"))
