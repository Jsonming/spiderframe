# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class VietnamNewsVnContentSpider(RedisSpider):
    name = 'vietnam_news_vn_content'
    allowed_domains = ['vnexpress.net']
    # start_urls = [
    #     'https://vnexpress.net/khoa-hoc/treo-tuong-tron-bang-chan-tac-ke-1963721.html',
    #
    # ]
    redis_key = 'vietnam_news_vn_link'
    custom_settings = {
        # 指定redis数据库的连接参数
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        # 指定 redis链接密码，和使用哪一个数据库
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        description = response.xpath('/html/body/section[2]/section[1]/section[1]/p/text()').extract()
        paragraph = response.xpath('/html/body/section[2]/section[1]/section[1]/article/p/text()').extract()
        content = ' '.join(description + paragraph).replace('\n', '')
        item = SpiderframeItem()
        item['url'] = response.url
        item['content'] = content
        return item
