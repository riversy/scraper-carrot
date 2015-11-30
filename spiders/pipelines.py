# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from scrapers.utils import MongoDBProvider

class SpidersPipeline(object):
    def __init__(self):
        self.session_timestamp = datetime.utcnow()

    def process_item(self, item, spider):
        item['_spider'] = spider.name
        item['_item'] = item.__class__.__name__
        item['_scraped_at'] = datetime.utcnow()
        item['_session_timestamp'] = self.session_timestamp
        return item

# noinspection PyMethodMayBeStatic,PyUnusedLocal
class MongoDBPipeline(MongoDBProvider):
    def open_spider(self, spider):
        self.logger.debug('open_spider')
        if self.database_available:
            idx_name = self.collection.create_index('url', unique=True, background=True)
            self.logger.info('Ensured for index (%s) exists' % idx_name)

    def close_spider(self, spider):
        self.logger.debug('open_close')
        if self.database_available:
            self.client.close()

    def process_item(self, item, spider):
        if self.database_available:
            try:
                find_query = {'url': item.get('url')}
                if self.collection.find_one(find_query):
                    self.collection.update(
                        spec=find_query,
                        document=dict(item),
                        upsert=True
                    )
                    self.stats.inc_value('mongodb/updated', spider=spider)
                else:
                    self.collection.insert_one(dict(item))
                    self.stats.inc_value('mongodb/inserted', spider=spider)
            except Exception as e:
                self.stats.inc_value('mongodb/errors', spider=spider)
                raise e

        return item
