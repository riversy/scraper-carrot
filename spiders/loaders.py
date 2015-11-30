from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class ScraperLoader(ItemLoader):
    default_output_processor = TakeFirst()
