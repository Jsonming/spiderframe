# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class NorwayAftenpostenContentSpider(RedisSpider):
    name = 'Norway_aftenposten_content'
    allowed_domains = ['www.aftenposten.no']
    start_urls = ['https://www.aftenposten.no/amagasinet/i/K31nge/julen-kan-vaere-lang-sosial-og-dyr-da-er-det-lov-aa-jukse-litt']

    redis_key = 'Norway_aftenposten_link'

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
