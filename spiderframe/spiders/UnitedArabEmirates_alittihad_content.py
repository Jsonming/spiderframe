# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class UnitedArabEmiratesAlittihadContentSpider(RedisSpider):
    name = 'UnitedArabEmirates_alittihad_content'
    allowed_domains = ['www.alittihad.ae']
    start_urls = ['https://www.alittihad.ae/article/76951/2018/%D9%81%D8%B1%D8%B6-%D8%BA%D8%B1%D8%A7%D9%85%D8%A9-%D8%B9%D9%84%D9%89-%D9%85%D8%A7%D8%B1%D8%A7%D8%AF%D9%88%D9%86%D8%A7-%D9%84%D8%AA%D8%B5%D8%B1%D9%8A%D8%AD%D8%A7%D8%AA%D9%87-%D8%B6%D8%AF-%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%8A%D9%85']

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

