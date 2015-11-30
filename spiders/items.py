# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

# noinspection PyAbstractClass
class ProductItem(Item):
    url = Field()
    name = Field()
    annotation = Field()
    price = Field()
    description = Field()
    attributes = Field()
    brand = Field()
    category = Field()
    image_urls = Field()
