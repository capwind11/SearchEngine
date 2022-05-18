# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


def create_news_item(title, time, content, source, url, cls):
    item = NewsItem()
    item['title'] = title
    item['date'] = time
    item['content'] = content
    item['source'] = source
    item['url'] = url
    item['cls'] = cls
    return item


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    cls = scrapy.Field()
