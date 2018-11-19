# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BroadcastEventItem(scrapy.Item):
    service = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    timezone = scrapy.Field()
    weekday = scrapy.Field()
    serie = scrapy.Field()


class ArticleItem(scrapy.Itme):
    title = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    section = scrapy.Field()
    service = scrapy.Field()
