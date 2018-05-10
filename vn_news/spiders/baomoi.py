from scrapy.spiders import CrawlSpider
import scrapy

from vn_news.spiders.baomoi_article import BaomoiArticleSpider


class BaomoiSpider(CrawlSpider):
    name = "baomoi"

    def start_requests(self):
        start_urls = [
            "http://www.baomoi.com/xa-hoi.epi",
            "http://www.baomoi.com/the-gioi.epi",
            "http://www.baomoi.com/van-hoa.epi",
            "http://www.baomoi.com/kinh-te.epi",
            "http://www.baomoi.com/giao-duc.epi",
            "http://www.baomoi.com/the-thao.epi",
            "http://www.baomoi.com/giai-tri.epi",
            "http://www.baomoi.com/phap-luat.epi",
            "http://www.baomoi.com/khoa-hoc-cong-nghe.epi",
            "http://www.baomoi.com/doi-song.epi",
            "http://www.baomoi.com/xe-co.epi",
            "http://www.baomoi.com/nha-dat.epi"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_parser = BaomoiArticleSpider()
        self.logger.info('==> %s', response.url)
        article_pages = response.xpath('').extract() # lay tat ca cac link trong page
        for next_page in article_pages:
            yield scrapy.Request(response.urljoin(next_page), callback=article_parser.parse)
