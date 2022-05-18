import scrapy
from ..items import NewsItem, create_news_item


class ChinadailySpider(scrapy.Spider):
    name = 'chinadaily'
    allowed_domains = ['chinadaily.com.cn']
    domains = ['china']
    root = 'https://www.chinadaily.com.cn/'
    start_urls = []
    for domain in domains:
        start_urls.append(root+domain)

    def parse(self, response):
        levelOfUrl = len(response.request.url.split('/'))-3
        if levelOfUrl==1:
            for href in response.xpath("//div[@class='topNav2_art']//a[@target='_top']/@href"):
                url = href.extract()
                for i in range(15):
                    newSite = 'https:'+url+'/page_{}.html'.format(i+1)
                    yield scrapy.Request(newSite, callback=self.parse)
        else:
            for href in response.xpath("//h4/a[@shape='rect']/@href"):
                url = href.extract()
                yield scrapy.Request('https:' + url, callback=self.parse_content)


    def parse_content(self, response):
        title = response.xpath("//h1/text()").extract()
        time = response.xpath("//span[@class='info_l']/text()").extract()
        content = response.xpath("//div[@id='Content']/p/text()").extract()
        cls = response.xpath("//span[@id='bread-nav']/a/text()").extract()
        item = create_news_item(title, time, content, self.name,response.request.url, cls)
        yield item
