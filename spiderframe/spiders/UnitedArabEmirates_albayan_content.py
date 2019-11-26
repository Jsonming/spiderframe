# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class UnitedArabEmiratesAlbayanSpider(RedisSpider):
    name = 'UnitedArabEmirates_albayan_content'
    allowed_domains = ['www.albayan.ae']
    start_urls = ['https://www.albayan.ae/across-the-uae/news-and-reports/2019-11-19-1.3705456']

    redis_key = 'UnitedArabEmirates_albayan_link'

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
        content = content.replace(" ","")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

