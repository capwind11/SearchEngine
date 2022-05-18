import scrapy

from ..items import NewsItem, create_news_item


class GlobaltimesSpider(scrapy.Spider):
    name = 'globaltimes'
    allowed_domains = ['globaltimes.cn']
    domains = ['china', 'source', 'opinion', 'hu-says', 'in-depth', 'world', 'life', 'sport']
    url_format = 'https://globaltimes.cn/{}/index.html'
    start_urls = []
    for domain in domains:
        start_urls.append(url_format.format(domain))

    def parse(self, response):
        for href in response.xpath("//div[@class='list_info']/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        title = response.xpath("//div[@class='article_title']/text()").extract()
        time = response.xpath("//span[@class='pub_time']/text()").extract()
        content = response.xpath("//div[@class='article_right']/text()").extract()
        cls = response.xpath("//div[@class='article_column']/span/a/text()").extract()

        # item['cls'] = "".join(cls[1:])
        item = create_news_item(title, time, content, self.name, response.request.url, cls)
        yield item
