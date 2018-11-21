import logging
import json

from graphqlclient import GraphQLClient
from scrapy.exporters import BaseItemExporter

def lower_first(s): return s[0].lower() + s[1:]


class PrismaGraphQLExporter(BaseItemExporter):
    create_query_pattern = '''
      mutation create($data: %sCreateInput!) {
        create%s(data: $data) { id }
      }
    '''

    def __init__(self, endpoint, typename=None, token=None, filter_field='id', fields_to_exoprt=[], **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.typename = typename
        self.fields_to_exoprt = fields_to_exoprt
        self.filter_field = filter_field
        self.prisma = GraphQLClient(endpoint)
        self.seen_relations = {}
        if token: self.prisma.inject_token(token)

    def export_item(self, item):
        existing_id = self._exists(item.get(self.filter_field), filter_field=self.filter_field)
        if existing_id:
            logging.info('Already exists in datbase, skip: %s', existing_id)
        else:
            logging.info('Create new object in database')
            self._execute_create(item)

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
        itemdict = dict(self._get_serialized_fields(item))
        # import pdb;pdb.set_trace()
        createQuery = self.create_query_pattern % (typename or self.typename, typename or self.typename)
        result = self.prisma.execute(createQuery, variables={'data': itemdict })
        logging.info('Executed create query: %s with result: %s and vatiables: %s', createQuery, result, itemdict)
        return result
