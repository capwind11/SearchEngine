# Press the green button in the gutter to run the script.
from api.search_api import app
from service.utils import *

if __name__ == "__main__":
    # crawl_news()
    download_news()
    build_inverted_index()
    app.run(host="0.0.0.0", port=5000, debug=True)