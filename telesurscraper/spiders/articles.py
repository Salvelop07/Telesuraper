from datetime import datetime
from extruct.w3cmicrodata import MicrodataExtractor
from extruct.jsonld import JsonLdExtractor
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urlparse import urljoin
import xml.sax.saxutils as saxutils
import logging

from telesurscraper.items import ArticleItem

mde = MicrodataExtractor()
jslde = JsonLdExtractor()

class HomeSpider(CrawlSpider):
    name='home'
    allowed_domains = ['telesurtv.net', 'telesurenglish.net']
    start_urls=[
        'https://www.telesurtv.net/'
    ]
    rules = (
        Rule(LinkExtractor(
            allow=(),
            deny=(
                r'multimedia/.+\.html$'
            ,)
        ), callback='parse_item'),
    )

    def parse_item(self, response):
        jsonld_meta = next(iter(filter(
            lambda obj: obj['@type'] == 'NewsArticle',
            jslde.extract(response.body)
        )), {})

        if jsonld_meta:
            item = ArticleItem(
                url=response.url,
                headline=saxutils.unescape(jsonld_meta.get('headline')),
                description=saxutils.unescape(jsonld_meta.get('description')),
                body=saxutils.unescape(response.css('.txt_newworld').extract_first()),
                datePublished=jsonld_meta.get('datePublished'),
            )
            yield item
