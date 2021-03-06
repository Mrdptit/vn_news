import re

from os.path import join, dirname
from scrapy.spiders import CrawlSpider


class BaomoiArticleSpider(CrawlSpider):
    name = "baomoi-reload"
    print("Crawing...")
    filepath = join(dirname(dirname(__file__)), "data", "crawled_urls.txt")
    start_urls = [line.strip() for line in open(filepath, "r").readlines()]

    def parse(self, response):
        self.logger.info('==> %s', response.url)
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