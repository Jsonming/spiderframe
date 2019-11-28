# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class PolandPolsatContentSpider(RedisSpider):
    name = 'Poland_polsat_content'""
    allowed_domains = ['www.polsat.pl']
    start_urls = ['https://www.polsat.pl/news/2016-03-18/aleksandra-szwed-jako-dawid-podsiadlo_1499684/']

    redis_key = 'Poland_polsat_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }


    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n","  ")
        content = content.replace("\t","  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

