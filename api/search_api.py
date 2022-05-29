from flask import Flask, request, render_template
from flask import jsonify
from service.search_service import *

#####################################################################################################################
###################################################以下部分为页面交互部分################################################

# global source,start_time, end_time, checked, page, resp
source = ['checked="true"', 'checked="true"', 'checked="true"', 'checked="true"', 'checked="true"']
checked = ['checked="true"', '', '']
start_time = ''
end_time = (datetime.date.today()).strftime("%Y-%m-%d")
resp = []
page = []

app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
    global source, start_time, end_time
    source = ['checked="true"', 'checked="true"', 'checked="true"', 'checked="true"', 'checked="true"']
    start_time = ''
    end_time = (datetime.date.today()).strftime("%Y-%m-%d")
    return render_template('search.html', error=True, start_time=start_time, end_time=end_time, source=source)

# 读取表单数据，获得doc_ID
@app.route('/search/', methods=['POST'])
def search_action():
    try:
        global keywords, start_time, end_time, source, checked
        keywords = request.form['key_word']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        sourcelist = ['foxnews', 'apnews', 'chinadaily', 'usatoday', 'globaltimes']
        source = []
        for item in sourcelist:
            try:
                check = request.form[item]
                source.append('checked="true"')
            except:
                source.append('')
                continue

        checked = ['checked="true"', '', '']

        if keywords not in ['']:
            # 这里等待api改成list
            # docs = search(keywords, source, start_time, end_time)
            s = sourcelist[0]
            docs = search(keywords, s, start_time, end_time)
            global resp, page
            resp = []
            for doc in docs:
                if len(doc[2])>=300:
                    snippet = doc[2][0:300]
                else:
                    snippet = doc[2]
                resp.append(
                    {
                        "id": doc[0],
                        "title": doc[1],
                        "content": doc[2],
                        "snippet": snippet + "……",
                        "source": doc[3],
                        "date": doc[4],
                        "url": doc[5],
                        "class": doc[6],
                    }
                )
            page = []
            for i in range(1, (len(resp) // 20 + 2)):
                page.append(i)
            docs = cut_page(page, 0, resp)
            return render_template('high_search.html', checked=checked, key=keywords, docs=docs, page=page,
                                   source=source, error=True,start_time=start_time, end_time=end_time)
        else:
            return render_template('search.html', error=False)
    except:
        print('search error')

@app.route('/search/page/<page_no>/', methods=['GET'])
def next_page(page_no):
    try:
        global checked, keywords, page, source, resp
        page_no = int(page_no)
        docs = cut_page(page, (page_no-1), resp)
        return render_template('high_search.html', checked=checked, key=keywords, docs=docs, page=page,
                               source=source, error=True, start_time=start_time, end_time=end_time)
    except:
        print('next error')

@app.route('/search/<id>/', methods=['GET', 'POST'])
def content(id):
    try:
        global resp
        for i in range(len(resp)):
            print(resp[i]["id"])
            if str(resp[i]["id"]) == id:
                doc = resp[i]
                return render_template('content.html', doc=doc)
    except:
        print('content error')

def cut_page(page, no, news):
    docs = news[no*20:page[no]*20]
    return docs

@app.route('/search/<key>/', methods=['POST'])
def high_search(key):
    try:
        global checked, keywords, start_time, end_time, resp, page
        selected = int(request.form['order'])
        for i in range(3):
            if i == selected:
                checked[i] = 'checked="true"'
            else:
                checked[i] = ''

        keywords = key
        #排序，按照Boolean、Date、Ranked,等待修改api
        # docs = search_rank(keywords, source, start_time, end_time, checked)
        s = source[0]
        docs = search(keywords, s, start_time, end_time)
        resp = []
        for doc in docs:
            if len(doc[2])>=300:
                snippet = doc[2][0:300]
            else:
                snippet = doc[2]
            resp.append(
                {
                    "id": doc[0],
                    "title": doc[1],
                    "content": doc[2],
                    "snippet": snippet + "……",
                    "source": doc[3],
                    "date": doc[4],
                    "url": doc[5],
                    "class": doc[6],
                }
            )
        page = []
        for i in range(1, (len(resp) // 20 + 2)):
            page.append(i)
        docs = cut_page(page, 0, resp)
        return render_template('high_search.html', checked=checked, key=keywords, docs=docs, page=page,
                               source=source, error=True, start_time=start_time, end_time=end_time)
    except:
        print('high search error')

#######################################################################################################################

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
