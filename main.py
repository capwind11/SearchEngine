# Press the green button in the gutter to run the script.
from api.search_api import app
from entity.global_entity import global_db
from service.utils import build_inverted_index, download_news


def init_data():
    download_news()  # 将db中的新闻下载到json中
    global_db.create_index_table()
    build_inverted_index()  # 建立倒排索引


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
