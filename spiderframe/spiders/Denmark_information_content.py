# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider

"Denmark_information_link"
class DenmarkInformationContentSpider(RedisSpider):
    name = 'Denmark_information_content'
    allowed_domains = ['www.information.dk']
    start_urls = ['https://www.information.dk/indland/2019/10/politiklagemyndighed-dropper-oversaettelser-omstridte-tolkefirma-easytranslate']

    redis_key = 'Denmark_information_link'

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

