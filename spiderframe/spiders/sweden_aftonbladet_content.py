# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class SwedenAftonbladeContentSpider(RedisSpider):
    name = 'sweden_aftonbladet_content'
    allowed_domains = ['www.aftonbladet.se/nyheter/trafik/a']
    start_urls = ['https://www.aftonbladet.se/nyheter/trafik/a/e8R3kg/singelolycka-orsakar-problem-pa-vag-154']

    redis_key = 'sweden_aftonbladet_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()

        item = SpiderframeItem()
        # item['id'] = 11111111111111
        item['url'] = response.url
        item['category'] = response.url.split('/')[-2]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        # print(item)
        yield item
