# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider

class NetherlandsAdContentSpider(RedisSpider):
    name = 'Netherlands_ad_content'
    allowed_domains = ['www.ad.nl']
    start_urls = ['https://www.ad.nl/binnenland/rutte-kan-wel-een-cursusje-leiderschap-gebruiken-van-georginio-wijnaldum~a45fe8db/']

    redis_key = 'Netherlands_ad_link'

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
        content = ''.join(content)
        content = content.replace(" ","")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

