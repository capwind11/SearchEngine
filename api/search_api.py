from flask import Flask, request
from flask import jsonify

from service.search_service import *

app = Flask(__name__)


@app.route("/api/boolean", methods=["GET"])
def boolean_search_api():
    keywords = request.args.get("keyword")
    keywords = keywords.split()
    docs = boolean_search(keywords)
    resp = []
    for doc in docs:
        resp.append({"docID": doc[0], "title": doc[1], "url": doc[2]})
    return jsonify(resp)


@app.route("/api/specific", methods=["GET"])
def specific_search_api():
    date_info = request.args.get("date")
    source = request.args.get("source")

    docs = specific_search(date_info, source)
    resp = []
    for doc in docs:
        resp.append({"docID": doc[0], "title": doc[1], "url": doc[2]})
    return jsonify(resp)
