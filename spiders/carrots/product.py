# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import os
from urllib import urlencode

import requests

from scrapy import Request

from scrapy.spiders import Spider

class CarrotProductSpider(Spider):

    allowed_domains = ['www.carrot.by']
    respect_nofollow = True
    start_urls = [
        "http://www.carrot.by/brends",
        "http://www.carrot.by/accessories",
        "http://www.carrot.by/rabochee_prostranstvo",
        "http://www.carrot.by/sweet_home",
        "http://www.carrot.by/gotovim",
        "http://www.carrot.by/Podarki",
        "http://www.carrot.by/hity",
        "http://www.carrot.by/Lifestyle",
        "http://www.carrot.by/latest",
        "http://www.carrot.by/sales"
    ]

    custom_settings = {
        'LOG_FILE': os.path.join(os.getcwd(), '.scrapy', '%s_%s.log' % (name, datetime.now())),
        'LOG_LEVEL': logging.INFO,

        'CONCURRENT_REQUESTS': 1,

        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_DEBUG': False,

        'HTTPCACHE_ENABLED': False,
        'HTTPCACHE_EXPIRATION_SECS': 60 * 60 * 24 * 31,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [503],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',

        'DOWNLOADER_MIDDLEWARES': {
            'scrapers.middlewares.MongoDBDownloadMiddleware': 100,
        },

        'ITEM_PIPELINES': {
            'scrapers.pipelines.MongoDBPipeline': 100,
        }
    }

    def parse_resume(self, response):
        l = ResumeLoader(item=ResumeItem(), response=response)

        l.add_value('url', response.url)
        l.add_xpath('birth_date', '//meta[@itemprop="birthDate"]/@content')
        l.add_xpath('gender', '//strong[@itemprop="gender"]/text()')
        l.add_xpath('locality', '//strong[@itemprop="addressLocality"]/text()')
        l.add_xpath('languages', u'//span[contains(text(),"Знание языков")]/../../following-sibling::div/text()')
        l.add_xpath('about_me', u'//span[contains(text(),"Обо мне")]/../../../div/string/text()')
        l.add_css('title', '.resume__position__title::text')
        l.add_css('salary', '.resume__position__salary::text')
        l.add_css('specialization', 'div.resume__position__specialization::text')
        l.add_css('specialization_area', 'div.resume__position__specialization_item::text')
        l.add_css('skills', '.Bloko-TagList-Text::text')

        additional_item_sel = response.css('.resume__additional-item')
        l.add_value('citizenship', additional_item_sel.xpath('span/span/text()').extract())
        l.add_value('work_permit', additional_item_sel.xpath('../div[2]/text()').extract())
        l.add_value('desired_travel_time_to_work', additional_item_sel.xpath('span/text()').extract())

        resume_block_sel = response.xpath('//div[@class="resume-block"]')
        l.add_value('busyness', resume_block_sel.xpath(u'div[contains(text(),"Занятость")]/text()').extract())
        l.add_value('schedule', resume_block_sel.xpath(u'div[contains(text(),"График работы")]/text()').extract())
        l.add_value('experience_total',
                    response.xpath(u'//span[contains(text(),"Опыт работы")]').re(ur'Опыт работы (.+)'))

        experience = []
        for sel in response.css('.resume__experience__item'):
            exp = ExperienceLoader(item=ExperienceItem(), selector=sel)
            exp.add_value('date', sel.css('.resume__experience__date').xpath('text()|span/text()').extract())
            exp.add_css('interval', '.resume__experience__timeinterval::text')
            exp.add_css('company', '.resume__experience__company::text')
            exp.add_css('position', '.resume__experience__position::text'),
            exp.add_xpath('company_locality', 'div//span[@itemprop="addressLocality"]/text()')
            exp.add_value('url', sel.css('.resume__experience__url').xpath('@href').extract())
            exp.add_value('industry', sel.css('.resume-industries').xpath('p/span/text()').extract()),
            exp.add_value('industry_areas', sel.css('.profareatree__subitem').xpath('span/text()').extract()),
            exp.add_value('description', sel.css('.resume__experience__desc').xpath('description/text()').extract()),
            experience.append(dict(exp.load_item()))
        l.add_value('experience', experience)

        education = []
        for sel in response.xpath('//*[@itemtype="http://schema.org/EducationalOrganization"]'):
            ed = EducationLoader(item=EducationItem(), selector=sel)
            ed.add_xpath('search_url', 'div/div[@itemprop="name"]/a/@href')
            ed.add_xpath('title', 'div/div[@itemprop="name"]/a/text()')
            ed.add_xpath('faculty', 'div/div[@class="resume__education__org"]/text()')
            ed.add_xpath('year', './preceding-sibling::td/text()')
            education.append(dict(ed.load_item()))
        l.add_value('education', education)

        yield l.load_item()
