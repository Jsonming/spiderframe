# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from spiderframe.items import SpiderframeItem


class HebrewWallaLinkSpider(scrapy.Spider):
    name = 'hebrew_walla_link'
    allowed_domains = ['www.walla.co.il']

    # redis_key = 'hebrew_walla_new_link'
    # custom_settings = {
    #     'REDIS_HOST': '123.56.11.156',
    #     'REDIS_PORT': 6379,
    #     'REDIS_PARAMS': {
    #         'password': '',
    #         'db': 0
    #     },
    # }

    def start_requests(self):
        for i in range(1000, 10000):
            url = 'https://news.walla.co.il/category/{}'.format(i)
            yield scrapy.Request(url=url, callback=self.parse, meta={'c_id': i})

    def parse(self, response):
        links = response.xpath("//section[(contains(@class, 'sequence'))]//a/@href").extract()
        for url in links:
            item = SpiderframeItem()
            item['url'] = url
            yield item

        if links:
            for y in range(2006, 2020):
                for m in range(1, 13):
                    url = 'https://news.walla.co.il/archive/{}?month={}&year={}'.format(response.meta.get('c_id'),
                                                                                        m, y)
                    yield scrapy.Request(url=url, callback=self.parse_item,
                                         meta={"page": 1, 'c_id': response.meta.get("c_id"), "month": m, 'year': y},
                                         dont_filter=True)

    def parse_item(self, response):
        links = response.xpath("//section[(contains(@class, 'sequence'))]//a/@href").extract()
        for url in links:
            item = SpiderframeItem()
            item['url'] = url
            yield item

        next_url = response.xpath('//section/div/nav[1]/a[@rel="next"]/@href').extract()
        if next_url:
            yield scrapy.Request(url=next_url[0], callback=self.parse_item, dont_filter=True)
