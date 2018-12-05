import logging
import json

from graphqlclient import GraphQLClient
from scrapy.exporters import BaseItemExporter

def lower_first(s): return s[0].lower() + s[1:]


class PrismaGraphQLExporter(BaseItemExporter):
    """Export data to a Prisma database"""

    def __init__(self, endpoint, typename=None, token=None, filter_field='id', fields_to_exoprt=[], **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.typename = typename
        self.fields_to_exoprt = fields_to_exoprt
        self.filter_field = filter_field
        self.prisma = GraphQLClient(endpoint)
        self.seen_relations = {}
        if token: self.prisma.inject_token(token)

    def export_item(self, item, update_existing=False):
        existing_id = self._exists(item.get(self.filter_field), filter_field=self.filter_field)
        if not existing_id:
            result = self._execute_create(item)
            logging.info('Created new Article, mutation result: %s', result)
        elif update_existing:
            result = self._execute_update(existing_id, item)
            logging.info('Updated existing Article, mutation result: %s', result)
        else:
            logging.debug('Already exists in datbase, skipping: %s', existing_id)

    def serialize_field(self, field, name, value):
        related_type = field.get('related_type')
        relation_field = field.get('relation_field')
        array_type = field.get('array_type')

        if not related_type:
            # This is a scalar field, return as is
            if array_type:
                return super().serialize_field(field, name, {'set': [*value]})
            else:
                return super().serialize_field(field, name, value)

        # This is a relation field, add or update related object if needed
        # TODO: remove code duplication
        if not array_type:
            seen_key = '%s:%s:%s' % (related_type, relation_field, value)

            related_obj = self.seen_relations.get('seen_key') \
                          or self._exists(value, filter_field=relation_field,
                                                 query_field=lower_first(related_type))
            self.seen_relations[seen_key] = related_obj

            # Create new related object if needed
            if not related_obj:
                related_obj = self._execute_create(dict(**{relation_field: value}), related_type)

            connection = {'connect': {'id': related_obj['id']}}
            return super().serialize_field(field, name, connection)

        else:
            connections = []
            for item_val in value:
                seen_key = '%s:%s:%s' % (related_type, relation_field, item_val)
                related_obj = self.seen_relations.get('seen_key') \
                              or self._exists(item_val, filter_field=relation_field,
                                                        query_field=lower_first(related_type))
                self.seen_relations[seen_key] = related_obj

                # Create new related object if needed
                if not related_obj:
                    related_obj = self._execute_create(dict(**{relation_field: item_val}), related_type)

                connections.append({'id': related_obj['id']})
            return super().serialize_field(field, name, {'connect': connections})

    def start_exporting(self):
        logging.info('start_exporting PrismaGraphQLExporter')

    def finish_exporting(self):
        logging.info('finish PrismaGraphQLExporter')

    def _exists(self, filter_value, filter_field='id', query_field=None):
        query_field = query_field or lower_first(self.typename)
        query = '{ %s(where: { %s: "%s" }) { id } }' % (
            query_field, filter_field, filter_value)
        result = json.loads(self.prisma.execute(query))

        return result['data'][query_field]

    def _execute_create(self, item, typename=None):
        typename = typename or self.typename
        query = '''
          mutation create($data: %sCreateInput!) {
            create: create%s(data: $data) { id }
          }
        ''' % (typename, typename)
        data = dict(self._get_serialized_fields(item))
        result = self.prisma.execute(query, variables=dict(data=data))
        logging.info('Executed create query: %s with result: %s', query, result)

        return json.loads(result)['data']['create']

    def _execute_update(self, item, id, typename=None):
        typename = typename or self.typename
        query = '''
          mutation update($where: %sWhereUniqueInput, $data: %sUpdateInput!) {
            create: update%s(data: $data) { id }
          }
        ''' % (typename, typename, typename)
        data = dict(self._get_serialized_fields(item))
        result = self.prisma.execute(query, variables=dict(data=data, where=dict(id=id)))
        logging.info('Executed update query: %s with result: %s', query, result)

        return json.loads(result)['data']['update']
