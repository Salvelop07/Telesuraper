from scrapy import Item, Field


class BroadcastEventItem(Item):
    service = Field()
    start = Field()
    end = Field()
    timezone = Field()
    weekday = Field()
    serie = Field()


# TODO: Autogenerate from GraphQL schema and/or introspect endpoint
class ArticleItem(Item):
    url = Field()
    datePublished = Field()
    headline = Field()
    description = Field()
    author = Field()
    body = Field()
    tags = Field(array_type=True)
    section = Field(related_type='ArticleSection', relation_field='name')
    images = Field(related_type='Image', relation_field='url', array_type=True)
    service = Field(related_type='Service', relation_field='name')
