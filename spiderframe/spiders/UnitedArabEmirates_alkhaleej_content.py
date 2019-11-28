# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class UnitedArabEmiratesAlkhaleejContentSpider(RedisSpider):
    name = 'UnitedArabEmirates_alkhaleej_content'
    allowed_domains = ['www.alkhaleej.ae']
    start_urls = ['http://www.alkhaleej.ae//Home/GetPage/f53c9315-c755-48f7-a351-9dc93baa2e5a/4238dbc0-8058-44c4-b7b1-6401c9eb8449']

    redis_key = 'UnitedArabEmirates_alittihad_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        title = response.xpath('//div[@class="Details_MainTitle"]/text()').extract()
        content = response.xpath('//div[@id="detailedBody"]//text()').extract()
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

