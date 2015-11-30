# -*- coding: utf-8 -*-

# Scrapy settings for employment project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_who_likes_carrots'

SPIDER_MODULES = ['spiders.carrots']
NEWSPIDER_MODULE = 'spiders.default'

MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DATABASE = 'carrot-garden'
MONGODB_COLLECTION = 'products'


# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
