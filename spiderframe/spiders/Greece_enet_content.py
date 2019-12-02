# -*- coding: utf-8 -*-
from spiderframe.items import SpiderframeItem
from scrapy import FormRequest
import scrapy
from scrapy_redis.spiders import RedisSpider

class GreeceEnetContentSpider(RedisSpider):
    name = 'Greece_enet_content'
    allowed_domains = ['www.enet.gr']
    start_urls = ['http://www.enet.gr/?i=issue.el.home&date=24/01/2010&id=124463']

    redis_key = 'Greece_enet_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h2[@class="page-title"]/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[-2]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

