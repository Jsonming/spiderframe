# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class NorwayDnContentSpider(RedisSpider):
    name = 'Norway_dn_content'
    allowed_domains = ['www.dn.no']
    start_urls = ['https://www.dn.no/d2/tekno/tekno/netflix/film/regissorlegende-med-filmens-svar-pa-deepfakes/2-1-708494']

    redis_key = 'Norway_dn_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h1//text()').extract()
        content = response.xpath('//p//text()').extract()
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
