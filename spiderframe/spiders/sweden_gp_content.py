# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class SwedenGpContentSpider(RedisSpider):
    name = 'sweden_gp_content'
    allowed_domains = ['www.gp.se']
    start_urls = ['https://www.gp.se/nyheter/sverige/utbildningsministern-vill-f%C3%B6rbjuda-religi%C3%B6sa-friskolor-saknar-st%C3%B6d-1.20815709']

    redis_key = 'sweden_gp_link'

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
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
