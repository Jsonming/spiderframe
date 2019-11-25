# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class FinlandHsContentSpider(RedisSpider):
    name = 'Finland_hs_content'
    allowed_domains = ['www.hs.fi']

    #     redis_key = 'Finland_hs_link'

    #
    # custom_settings = {
    #     'REDIS_HOST': '123.56.11.156',
    #     'REDIS_PORT': 6379,
    #     'REDIS_PARAMS': {
    #         'password': '',
    #         'db': 0
    #     },
    # }
    def start_requests(self):
        import pymysql
        conn = pymysql.connect(
            host='123.56.11.156',
            port=3306,
            user='sjtUser',
            passwd='sjtUser!1234',
            db='spiderframe',
            charset='utf8',
        )

        with conn.cursor() as cursor:
            sql = "select url from Finland_hs_content11;"
            cursor.execute(sql)
            while True:
                conn.ping()
                result = cursor.fetchone()
                if result:
                    url = result[0]
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        title = response.xpath('//h1[contains(@class, "title")]/text()').extract()
        content = response.xpath('//div[@class="body"]//text()').extract()

        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
