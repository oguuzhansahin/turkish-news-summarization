import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner
import extruct

def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class WebteknoCrawler(CrawlSpider):
    name = 'webtekno'
    allowed_domains = ['www.webtekno.com']
    start_urls = ['https://www.webtekno.com/haber']
    rules = (
        Rule(
            LinkExtractor(
                deny=[
                    re.escape('https://www.webtekno.com/video'),
                    re.escape("https://www.webtekno.com/uye/sifremi-unuttum"),
                    re.escape("https://www.webtekno.com/iletisim"),
                    re.escape("https://www.webtekno.com/kunye")
                    
                ],
            ),
            process_links=process_links,
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        return {
            'url': response.url,       
        }