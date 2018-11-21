# -*- coding: utf-8 -*-
from dateutil.parser import parse
from graphqlclient import GraphQLClient
import logging
import json
from scrapy.exporters import PythonItemExporter
from htmlmin import minify
from tomd import Tomd

from telesurscraper.exporters import PrismaGraphQLExporter

class PrismaArticlePipeline(object):

    def process_item(self, item, spider):
        item['service'] = 'teleSUR'
        exporter = PrismaGraphQLExporter(
            typename='Article',
            filter_field='url',
            endpoint=spider.settings['PRISMA_ENDPOINT'],
            token=spider.settings['PRISMA_TOKEN']
            )
        exporter.start_exporting()
        id = exporter.export_item(item)
        print('Got ID:', id)
        if id:
            logging.info('Exported object id: %s', id)
            return item
        else:
            logging.info('Item not exported: %s', item)
