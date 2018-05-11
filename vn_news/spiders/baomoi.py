from scrapy.spiders import CrawlSpider
import scrapy
from scrapy.selector import Selector
from vn_news.items import VnNewsItem
from vn_news.spiders.baomoi_article import BaomoiArticleSpider

xpath_thumb = '//div[@class="story__thumb"]/a/@href'
xpath_get_next_Page = '//a[@class="control__next"]/@href'
class BaomoiSpider(CrawlSpider):
    name = "baomoi"
    allowed_domains = ['http://www.baomoi.com']
    print("connecting....")
    
    
    def __init__(self, *args, **kwargs):
        super(BaomoiSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.baomoi.com/xa-hoi.epi',]

    def start_requests(self):
        print("=============== Starting ==================")
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
            #self.logger.info('==> %s', url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #self.logger.info('==> %s', response.url)
        print("=========================================")
        article_pages = response.xpath(xpath_thumb).extract()
        #print(article_pages)
        for next_page in article_pages:
            article_parser = BaomoiArticleSpider()
            article_parser.start_urls = article_pages
            #self.logger.info('==> link crawling: %s', response.urljoin(next_page))
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_data)
            pass
    def parse_page(self, response):
        article_pages = response.xpath(xpath_get_next_Page).extract()
        
    def parse_data(self, response):
        print('============ Crawling ===============')
        print('==> %s', response.url)
        url = response.url
        id = re.compile(".*/(\d+).epi").match(url).groups()[0]
        content = response.css(".article__sapo ::text").extract_first()
        body_text = response.css(".body-text")
        for text in body_text:
            text_content = text.css("::text").extract()
            if type(text_content) == list:
                text_content = u"".join(text_content)
            content += text_content + " "
        content = content.strip()
        title = response.css("h1 ::text").extract_first()
        yield {"url": url, "id": id, "title": title, "content": content}