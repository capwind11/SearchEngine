from flask import Flask, request
from flask import jsonify

from service.search_service import *

app = Flask(__name__)


@app.route("/api/boolean", methods=["GET"])
def boolean_search_api():
    keywords = request.args.get("keyword")
    docs = boolean_search(keywords)
    resp = []
    for doc in docs:
        resp.append({"docID": doc[0], "title": doc[1], "url": doc[2]})
    return jsonify(resp)


# 根据日期区间查找，从begin到end的所有新闻
@app.route("/api/specific", methods=["GET"])
def specific_search_api():
    date_begin = request.args.get("begin")
    date_end = request.args.get("end")
    source = request.args.get("source")

    docs = specific_search_by_period(date_begin, date_end, source)
    resp = []
    for doc in docs:
        resp.append({"docID": doc[0], "title": doc[1], "url": doc[2], "date": doc[3]})
    return jsonify(resp)


# 距离今天interval时间段内的新闻
@app.route("/api/interval", methods=["GET"])
def interval_search_api():
    interval = request.args.get("interval")
    source = request.args.get("source")

    docs = specific_search_by_date_interval(interval, source)
    resp = []
    for doc in docs:
        resp.append({"docID": doc[0], "title": doc[1], "url": doc[2], "date": doc[3]})
    return jsonify(resp)
