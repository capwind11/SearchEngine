from flask import Flask, request
from flask import jsonify

from service.search_service import *

app = Flask(__name__)


@app.route("/api/search", methods=["GET"])
def search_api():
    keywords = request.args.get("keyword")
    date_begin = request.args.get("begin")
    date_end = request.args.get("end")
    interval = request.args.get("interval")
    source = request.args.get("source")
    docs = search(keywords, source, date_begin, date_end, interval)
    resp = []
    for doc in docs:
        resp.append(
            {
                "title": doc[1],
                "content": doc[2],
                "source": doc[3],
                "date": doc[4],
                "url": doc[5],
                "class": doc[6],
            }
        )
    return jsonify(resp)
