from extruct.jsonld import JsonLdExtractor
from extruct.w3cmicrodata import MicrodataExtractor
from jmespath import search as search_jmespath
from scrapy.loader import ItemLoader


class ExtructItemLoader(ItemLoader):
    """Extracts JSON+LD and Microdata metadata
       with jmespath queries"""

    def __init__(self, *args, **kwargs):
        self.jsonld = JsonLdExtractor().extract(kwargs['response'].body)
        self.microdata = MicrodataExtractor().extract(kwargs['response'].body)

        return super(ExtructItemLoader, self).__init__(*args, **kwargs)

    def add_jsonld(self, field_name, typename, jmespath, *processors, **kwargs):
        query = '[?"@type"==`{}`] | {}'.format(typename, jmespath)
        value = search_jmespath(query, self.jsonld)

        return self.add_value(field_name, value, *processors, **kwargs)
