# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from dateutil import parser

from db.news_database import NewsDB


def preprocessing(item):
    title = item.get("title", "")[0]
    cls = " ".join([s.strip() for s in item.get("cls", "")])
    url = item.get("url", "")

    if "foxnews" in url and len(url.split("/")) > 3:
        cls = url.split("/")[3] + " " + cls
    content = " ".join([s.strip() for s in item.get("content", "")])

    time_string = (
        item.get("date", "")[0].replace("Published: ", "").replace("Published", "")
    )
    if "Updated:" in time_string:
        if "chinadaily" in url:
            time_string = time_string.split("Updated:")[1].strip()
        else:
            time_string = time_string.split("Updated:")[0].strip()

    date_object = parser.parse(time_string).date()
    return {
        "title": title,
        "content": content,
        "source": item.get("source", ""),
        "url": url,
        "cls": cls,
        "date": str(date_object),
    }


class CrawlerPipeline:
    def process_item(self, item, spider):
        news = preprocessing(item)
        docId = self.infodb.insert_news(
            news["title"],
            news["date"],
            news["content"],
            news["source"],
            news["url"],
            news["cls"],
        )
        news["id"] = docId
        if docId < 10:
            print()
        json.dump(news, self.f, indent=2)
        if docId < 10:
            print()
        # newsJson = json.dumps(news, indent=1)
        self.f.write(",\n")
        return item

    def open_spider(self, spider):
        self.f = open("../../data/news.json", "w", newline="\n")
        self.f.write("[")
        self.infodb = NewsDB()
        self.infodb.open_db()
        self.infodb.create_news_table()
        self.infodb.create_index_table()

    def close_spider(self, spider):
        self.infodb.close_db()
        self.f.write("{}]")
        self.f.close()
