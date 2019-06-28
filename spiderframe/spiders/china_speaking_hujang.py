# -*- coding: utf-8 -*-
import scrapy


class ChinaSpeakingHujangSpider(scrapy.Spider):
    name = 'china_speaking_hujang_link'
    allowed_domains = ['www.hjenglish.com/yanjiang/tedyanjiang']
    start_urls = ['http://www.hjenglish.com/yanjiang/tedyanjiang/']

    def parse(self, response):
        pass
