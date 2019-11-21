# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class GreeceTaneaContentSpider(RedisSpider):
    name = 'Greece_tanea_content'
    allowed_domains = ['www.tanea.gr']
    start_urls = ['https://www.tanea.gr/2019/11/21/greece/employment/syntakseis-poioi-dimosioi-ypalliloi-vgainoun-noritera-apo-tin-ergasia-tous/']

    redis_key = 'Greece_tanea_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h1[contains(@class, "title")]/text()').extract()
        content = response.xpath('//span/text()').extract()

        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[6]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
