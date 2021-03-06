# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class DenmarkJyllandsContentSpider(RedisSpider):
    name = 'Denmark_jyllands_content'
    allowed_domains = ['jyllands-posten.dk']
    start_urls = ['https://jyllands-posten.dk/debat/blogs/camillaburgwald/ECE11698930/hjernen-har-brug-for-ro-og-hvile-men-teenagere-er-online-op-til-seks-timer-om-dagen-hvem-skal-laere-dem-at-slukke/']

    redis_key = 'Denmark_jyllands_link'

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

