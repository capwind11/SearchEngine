# Press the green button in the gutter to run the script.
from api.search_api import app
from entity.global_entity import global_db
from service.utils import build_inverted_index

if __name__ == "__main__":
    # crawl_news()
    global_db.create_index_table()
    # download_news()
    build_inverted_index()
    app.run(host="0.0.0.0", port=5000, debug=True)
