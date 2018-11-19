# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from dateutil.parser import parse
from graphqlclient import GraphQLClient
import logging
import json
from scrapy.exporters import PythonItemExporter
from htmlmin import minify
from tomd import Tomd


class PrismaItemPipeline(object):
    def open_spider(self, spider):
        print('PAPAPA', spider.settings['PRISMA_ENDPOINT'])
        self.prisma = GraphQLClient(spider.settings['PRISMA_ENDPOINT'])
        token = spider.settings['PRISMA_TOKEN']
        if token: self.prisma.inject_token(token)

        logging.info("Opening Prisma GraophQL spider with client: %s", self.prisma)

    def close_spider(self, spider):
        logging.info("Closing Prisma GraphQL spider")

    def find_item(self, item):
        if isinstance(item['url'], basestring):
            logging.warning('Invlid URL: %s', item['url'])
            return None
        query = '''
        {{
          {query_field} (
            where: {{ {self.filter_arg}: "{filter_value}" }}
          ) {{
            {self.fragment}
          }}
        }}
        '''.format(
            self=self,
            query_field=self.typename.lower(),
            filter_value=item[self.filter_arg]
            )

        return self._execute_query(query, self.typename.lower())

    def create_item(self, item):
        mutation = '''
        mutation ($data: {self.typename}CreateInput!) {{
          create{self.typename}(data: $data) {{
            {self.fragment}
          }}
        }}
        '''.format(self=self)

        return self._execute_query(
            mutation, self.typename.lower(),
            variables={'data': self.input_data(item)}
            )

    def update_item(self, item):
        return self._execute_query(query, 'update%s' % self.typename)

    def delete_item(self, item):
        return self._execute_query(query, 'update%s' % self.typename)

    def _execute_query(self, query, result_field, variables={}):
        result = json.loads(self.prisma.execute(query, variables=dict(variables)))
        logging.info('Executing GraphQL query: %s', query)
        logging.info('With variables: %s', variables)
        logging.info('Gestting GraphQL result: %s', result)
        return (result['data'] or {}).get(result_field)


class ArticlePipeline(PrismaItemPipeline):
    typename = 'Article'
    filter_arg = 'url'
    fragment = '''headline, datePublished, body'''

    def input_data(self, item):
        body = minify(item['body']).strip()
        data = dict(
            service={'connect': {'name': 'teleSUR'}},
            url=item['url'],
            datePublished=parse(item['datePublished']).isoformat(),
            headline=item['headline'],
            bodySource=item['body'],
            body=body,
            bodyMarkdown=Tomd(body.encode('utf-8')).markdown,
            description=item['description'],
            author="teleSUR",
            )
        print('ESS', data)
        return data

    def process_item(self, item, spider):
        existing = self.find_item(item)

        if existing:
            logging.info('Ya existe')
        else:
            logging.info('Article not found in database. Create new')
            return self.create_item(item)

        return item


class BroadcastEventPipeline():
    def process_item(self, item, spider):
        return item
