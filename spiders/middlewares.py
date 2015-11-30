from scrapy.exceptions import IgnoreRequest
from spiders.utils import MongoDBProvider

class MongoDBDownloadMiddleware(MongoDBProvider):
    def process_request(self, request, spider):
        if not self.database_available:
            return

        item = self.collection.find_one({'url': request.url}, {'_id': 1})
        if item:
            self.stats.inc_value('mongodb/ignore', spider=spider)
            raise IgnoreRequest('Item (%s) found in database by url (%s)' % (item.get('_id', 'NO_ID'), request.url))
