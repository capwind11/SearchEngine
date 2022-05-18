import scrapy
from ..items import NewsItem, create_news_item


class UsatodaySpider(scrapy.Spider):
    name = 'usatoday'
    allowed_domains = ['usatoday.com']
    start_urls = []
    url_set = set()
    root = 'https://www.usatoday.com'
    domains = ['news', 'sports', 'entertainment', 'life', 'money', 'tech'
               'travel', 'opinion']
    for domain in domains:
        start_urls.append(root+'/'+domain)


    def parse(self, response):
        level = len(response.request.url.split('/'))-2
        if level <= 3:
            for href in response.xpath("//div[@class='gnt_m_bdl_t']/a/@href"):
                url = href.extract()

                yield scrapy.Request(self.root + url, callback=self.parse)

        for href in response.xpath("//div[@class='gnt_m gnt_m_flm']/a/@href"):
            url = href.extract()
            if 'video' in url:
                continue
            if url in self.url_set:
                continue
            self.url_set.add(url)
            yield scrapy.Request(self.root + url, callback=self.parse_content)


    def parse_content(self, response):

        title = response.xpath("//h1/text()").extract()
        time = response.xpath("//div[@class='gnt_ar_dt']/@aria-label").extract()
        content = response.xpath("//div[@class='gnt_ar_b']/p/text()").extract()
        cls = response.xpath("//a[@class='gnt_ar_lbl_a']/text()").extract()

        # item['cls'] = "".join(cls[1:])
        item = create_news_item(title, time, content, self.name, response.request.url, cls)
        yield item

