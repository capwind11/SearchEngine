from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

SPIDER_NAMES = ["globaltimes", "foxnews", "chinadaily", "apnews", "usatoday"]


def crawl_all(spider_names=SPIDER_NAMES):
    process = CrawlerProcess(get_project_settings())
    for spider in spider_names:
        process.crawl(spider)
    process.start()


def crawl_news():
    crawl_all(SPIDER_NAMES)
