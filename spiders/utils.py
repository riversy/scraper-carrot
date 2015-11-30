# coding=utf-8
import logging
import phonenumbers
from pymongo import MongoClient
import re

class MongoDBProvider(object):
    database_available = True

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('MONGODB_URI'),
            db=crawler.settings.get('MONGODB_DATABASE'),
            collection=crawler.settings.get('MONGODB_COLLECTION'),
            stats=crawler.stats
        )

    def __init__(self, uri, db, collection, stats):
        self.stats = stats
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Initializing connection to MongoDB. Please wait...')
        try:
            self.client = MongoClient(uri, connectTimeoutMS=1000, serverSelectionTimeoutMS=1000)
            self.db = self.client[db]
            self.collection = self.db[collection]
            self.logger.info(
                'Connection to MongoDB established, collection size = %d' % self.collection.count())
        except Exception as e:
            self.logger.error('Exception on init MongoDBSpiderMiddleware: %s' % e.message)
            self.database_available = False


def only_digits(data):
    return filter(unicode.isdigit, data)

def parse_currency(data):
    value, currency = data.split(' ')
    return {
        'value': only_digits(value),
        'currency': currency
    }

def parse_colon_separated_value(data):
    _, permit = data.split(': ')
    return permit

def parse_languages(data):
    language, level = data.split(unichr(8212))  # unichr(8212) = '—' (double dash)
    return {
        'language': language.strip(),
        'level': level.strip()
    }

re_space_chain = re.compile('\s{2,}')

def normalize_spaces(data):
    return re_space_chain.sub(' ', data)
