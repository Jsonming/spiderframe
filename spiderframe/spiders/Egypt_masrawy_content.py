# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class EgyptMasrawyContentSpider(RedisSpider):
    name = 'Egypt_masrawy_content'
    allowed_domains = ['www.masrawy.com']
    start_urls = ['https://www.masrawy.com/news/news_cases/details/2019/11/18/1672863/%D8%AA%D8%AC%D8%AF%D9%8A%D8%AF-%D8%AD%D8%A8%D8%B3-%D8%A7%D9%84%D9%85%D8%AA%D9%87%D9%85-%D9%81%D9%8A-%D8%AD%D8%A7%D8%AF%D8%AB-%D9%85%D8%B9%D9%87%D8%AF-%D8%A7%D9%84%D8%A3%D9%88%D8%B1%D8%A7%D9%85-15-%D9%8A%D9%88%D9%85%D8%A7-%D8%B9%D9%84%D9%89-%D8%B0%D9%85%D8%A9-%D8%A7%D9%84%D8%AA%D8%AD%D9%82%D9%8A%D9%82%D8%A7%D8%AA#SectionMore']

    redis_key = 'Egypt_masrawy_link'

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

        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[4]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        # print(item)
        yield item

