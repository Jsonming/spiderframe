# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class NorwayDagbladetContentSpider(RedisSpider):
    name = 'Norway_dagbladet_content'
    allowed_domains = ['www.dagbladet.no']
    start_urls = ['https://www.dagbladet.no/nyheter/politiets-skrekktall---helt-sjukt/71812219']

    redis_key = 'Norway_dagbladet_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h2/text()').extract()
        content = response.xpath('//p/text()').extract()

        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        # print(item)
        yield item

