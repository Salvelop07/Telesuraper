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
    dateModified = Field()
    headline = Field()
    description = Field()
    author = Field()
    body = Field()
    tags = Field(array_type=True)
    images = Field(array_type=True)
    sections = Field(array_type=True, related_type='ArticleSection', relation_field='name')
    service = Field(related_type='Service', relation_field='name')
