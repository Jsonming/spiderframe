# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class SwedenSydsvenskanContentSpider(RedisSpider):
    name = 'sweden_sydsvenskan_content'
    allowed_domains = ['www.sydsvenskan.se']
    start_urls = ['https://www.sydsvenskan.se/2019-11-25/elever-pa-nyrenoverade-bergaskolan-vi-har-ingenstans-att']

    redis_key = 'sweden_sydsvenskan_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//h2//text()').extract()
        content = response.xpath('//div[@class="article-text"]/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
