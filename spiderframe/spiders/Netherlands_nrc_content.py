# -*- coding: utf-8 -*-
from spiderframe.items import SpiderframeItem
from scrapy import FormRequest
import scrapy
from scrapy_redis.spiders import RedisSpider

class NetherlandsNrcContentSpider(RedisSpider):
    name = 'Netherlands_nrc_content'
    allowed_domains = ['www.nrc.nl']
    start_urls = ['https://www.nrc.nl/nieuws/2019/11/28/onderzoeksraad-rijhulpsystemen-autos-nog-niet-veilig-genoeg-a3981976']

    redis_key = 'Netherlands_nrc_link'

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

