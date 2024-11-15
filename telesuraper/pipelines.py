# -*- coding: utf-8 -*-
import json
import logging

from graphqlclient import GraphQLClient
from htmlmin import minify
from scrapy.exporters import PythonItemExporter

from Telesuraper.exporters import PrismaGraphQLExporter


class PrismaArticlePipeline(object):
    """Article pipeline"""

    def open_spider(self, spider):
        self.exported = []
        self.skipped = []

    def close_spider(self, spider):
        logging.info('Closping spider, total exported: {}, total skipped: {}'.format(
            len(self.exported), len(self.skipped)))

    def process_item(self, item, spider):
        item['service'] = getattr(spider, 'service_name', 'teleSUR')
        exporter = PrismaGraphQLExporter(
            typename='Article',
            filter_field='url',
            endpoint=spider.settings['PRISMA_ENDPOINT'],
            token=spider.settings['PRISMA_TOKEN']
        )
        exporter.start_exporting()
        id = exporter.export_item(item)
        if id:
            logging.info('Exported object id: %s', id)
            self.exported.append(id)
            return item
        else:
            logging.info('Item not exported: %s', item['url'])
            self.skipped.append(id)
