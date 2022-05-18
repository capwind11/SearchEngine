import scrapy
import json
from ..items import NewsItem, create_news_item


class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com']
    root = 'https://foxnews.com/'
    api = 'https://www.foxnews.com/api/article-search?searchBy=categories&values=fox-news%2F{}&size={}&from={}'
    domains = ['us', 'politics', 'media', 'opinion', 'entertainment', 'sport']
    url_set = set()
    start_urls = []
    for domain in domains:
        for i in range(100):
            start_urls.append(api.format(domain, 30, 30*i))

    def parse(self, response):
        newsList = json.loads(response.text)
        for news in newsList:
            url = news['url']
            if 'video' in url or url in self.url_set:
                continue
            self.url_set.add(url)
            yield scrapy.Request(self.root+url, callback=self.parse_content)

    def parse_content(self, response):
        title = response.xpath("//h1[@class='headline']/text()").extract()
        time = response.xpath("//div[@class='article-date']/time/text()").extract()
        content = response.xpath("//div[@class='article-body']/p/text()").extract()
        cls = response.xpath("//div[@class='eyebrow']/a/text()").extract()

        # item['cls'] = "".join(cls[1:])
        item = create_news_item(title, time, content, self.name, response.request.url, cls)
        yield item
