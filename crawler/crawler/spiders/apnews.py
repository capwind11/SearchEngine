import scrapy
from ..items import NewsItem, create_news_item


class ApnewsSpider(scrapy.Spider):
    name = 'apnews'
    allowed_domains = ['apnews.com']
    root = 'https://apnews.com/hub/'
    start_urls = ['https://apnews.com', 'https://apnews.com/hub/us-news']



    def parse(self, response):
        prefix = 'https://apnews.com'
        level = len(response.request.url.split('/'))-2
        if level == 1:
            for href in response.xpath("//*[@id='root']/div/main/div[1]/div[2]/div/ol/li/span/a/@href"):
                url = href.extract()
                yield scrapy.Request(prefix + url, callback=self.parse)
        else:
            for href in response.xpath("//a[@data-key='card-headline']/@href"):
                url = href.extract()
                yield scrapy.Request(prefix + url, callback=self.parse_content)


    def parse_content(self, response):
        title = response.xpath("//h1/text()").extract()
        time = response.xpath("//span[@data-key='timestamp']/@data-source").extract()
        content = response.xpath("//div[@class='Article']/p/text()").extract()
        cls = response.xpath("//div[@class='article_column']/span/a/text()").extract()
        item = create_news_item(title, time, content, self.name, response.request.url, cls)
        yield item
