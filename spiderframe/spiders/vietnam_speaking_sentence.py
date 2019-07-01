# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from spiderframe.items import SpiderframeItem


class VietnamSpeakingSentenceSpider(RedisSpider):
    name = 'vietnam_speaking_sentence'
    # allowed_domains = ['vi.glosbe.com']
    # start_urls = ['https://vi.glosbe.com/zh/vi/爸爸']
    redis_key = 'vietnam_speaking_url'
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        nodes = response.xpath('//*[@id="tmTable"]/div/div[2]/span/span')
        for node in nodes:
            sentence = ''.join(node.xpath(".//span/text()").extract())
            item = SpiderframeItem()
            item['url'] = response.url
            item['content'] = sentence
            yield item
