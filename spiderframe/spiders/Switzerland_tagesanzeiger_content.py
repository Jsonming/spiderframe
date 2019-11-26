# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class SwitzerlandTagesanzeigerContentSpider(RedisSpider):
    name = 'Switzerland_tagesanzeiger_content'
    allowed_domains = ['www.tagesanzeiger.ch']
    start_urls = ['https://www.tagesanzeiger.ch/ausland/amerika/die-impeachmentanhoerungen-im-ueberblick/story/15274899']

    redis_key = 'Switzerland_tagesanzeiger_link'

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
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        # print(item)
        yield item
