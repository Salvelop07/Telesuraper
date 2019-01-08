from datetime import datetime
from html import unescape
import logging

from dateutil.parser import parse as parse_date
import htmlmin
from scrapy import Request
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose, Identity

from telesurscraper.itemloaders import ExtructItemLoader
from telesurscraper.items import ArticleItem


class ArticlePageItemLoader(ExtructItemLoader):
    default_input_processor = MapCompose(unescape)
    default_output_processor = TakeFirst()

    body_in = MapCompose(default_input_processor, htmlmin.minify)

    tags_out = Identity()

    images_out = Identity()

    sections_out = Identity()

    author_in = MapCompose(str.strip)

    datePublished_in = MapCompose(parse_date, lambda date: date.isoformat())

    dateModified_in = MapCompose(parse_date, lambda date: date.isoformat())


class BaseArticlePageSpider(Spider):
    """Load data from an Article Page
    Example URL: https://www.telesurtv.net/news/muere-ali-rodriguez-araque-venezuela-cuba-20181119-0040.html"""

    def parse_article_page(self, response):
        l = ArticlePageItemLoader(item=ArticleItem(), response=response)

        # URL
        l.add_value('url', response.url)

        # Headline
        l.add_jsonld('headline', 'NewsArticle', '[].headline')
        l.add_css('headline', '[itemprop=headline]')

        # Date published/modified
        l.add_jsonld('datePublished', 'NewsArticle', '[].datePublished')
        l.add_jsonld('dateModified', 'NewsArticle', '[].dateModified')

        # Description
        l.add_jsonld('description', 'NewsArticle', '[].description')

        # Author
        l.add_jsonld('author', 'NewsArticle', '[].author.name')

        # Images
        l.add_jsonld('images', 'NewsArticle', '[].image.url')

        # Body
        l.add_css('body', '.txt_newworld')

        # Sections
        l.add_css('sections', '.nworldtop .itacaput a::attr(title)')

        # Tags
        l.add_css('tags', '.tagBarNews a::attr(title)')

        item = l.load_item()

        return item


class ArticleJspListingSpider(BaseArticlePageSpider):
    """Follows Article links from website's listing view endpoint"""

    name = 'article-jsplisting'

    def start_requests(self):
        page_size = int(getattr(self, 'page_size', self.settings.get('JSPLISTING_PAGE_SIZE', 20)))
        max_pages = int(getattr(self, 'max_pages', self.settings.get('JSPLISTING_MAX_PAGES', 10)))
        page = getattr(self, 'page', 1)

        service_name = getattr(self, 'service_name', 'teleSUR')
        default_url = 'https://www.telesurtv.net/system/modules/com.tfsla.diario.telesur/elements/TS_NewsCategory_Page.jsp'
        if service_name == 'teleSUR English':
            default_url = 'https://www.telesurenglish.net/system/modules/com.tfsla.diario.telesur.en/elements/TS_NewsCategory_Page.jsp'
        jsp_url = self.settings.get('JSPLISTING_PAGE_URL', default_url)

        for i in range(max_pages):
            url = '{}?pagina={}&size={}'.format(jsp_url, i+page, page_size)
            yield Request(url, callback=self.parse_article_links)

    def parse_article_links(self, response):
        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse_article_page)

class HomeCrawlerSpider(CrawlSpider, BaseArticlePageSpider):
    """Follows Article links from Home 's listing view endpoint"""

    name='home'

    allowed_domains = ['telesurtv.net', 'telesurenglish.net']
    start_urls = ['https://www.telesurtv.net/']
    rules = [
        Rule(LinkExtractor(deny=(r'multimedia/.+\.html$',)),
             callback='parse_article_page')
    ]
