# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider

class DenmarkPolitikenContentSpider(RedisSpider):
    name = 'Denmark_politiken_content'
    allowed_domains = ['politiken.dk']
    start_urls = ['https://politiken.dk/podcast/bogfolk/art6261614/Rejs-med-ind-i-b%C3%B8rneb%C3%B8gernes-verden']

    redis_key = 'Denmark_politiken_link'

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
        item['content'] = content
        # print(item)
        yield item

