# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class ChinaNewsPeopleContentSpider(RedisSpider):
    name = 'china_news_people_content'
    allowed_domains = ['culture.people.com']
    start_urls = [
        # 'http://politics.people.com.cn/n1/2019/0701/c1024-31204325.html',
        "http://politics.people.com.cn/n1/2019/0620/c1001-31170789.html"
    ]

    redis_key = 'china_news_people_link'
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        content = response.xpath('//div[@class="box_con"]/p/text()').extract()
        text = ''.join(content).replace('\r', '').replace('\n', '').replace('\t', '')
        item = SpiderframeItem()
        item["url"] = response.url
        item["content"] = text
        yield item
