# Press the green button in the gutter to run the script.
from api.search_api import app
from entity.global_entity import global_db
from service.ranked_service import process_tfidf
# from service.cls_service import classify_docs
from service.utils import build_inverted_index, download_news, reconstruct_news


def init_data(cls_dict=None):

    # if cls_dict is not None:
    #     classify_docs(weights_path=cls_dict['weights_path'],
    #                   device=cls_dict['device'], save=True)
    reconstruct_news()  # 将db中的新闻重构并下载到json中
    process_tfidf()
    global_db.create_index_table()
    build_inverted_index()  # 建立倒排索引



if __name__ == "__main__":
    # init_data() # 第一次运行时要执行，用于构建倒排索引及tfidf等文件
    app.run(host="0.0.0.0", port=5000, debug=True)
