# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class FinlandHsContentSpider(RedisSpider):
    name = 'Finland_hs_content'
    allowed_domains = ['www.hs.fi']
    start_urls = ['https://www.hs.fi/kaupunki/art-2000006306090.html']

    redis_key = 'Finland_hs_link'

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
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
