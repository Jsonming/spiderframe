# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class GreeceTaneaContentSpider(RedisSpider):
    name = 'Greece_tanea_content'
    allowed_domains = ['www.tanea.gr']

    redis_key = 'Greece_tanea_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }
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
            sql = "select url from Greece_tanea_content1;"
            cursor.execute(sql)
            while True:
                conn.ping()
                result = cursor.fetchone()
                if result:
                    url = result[0]
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[6]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
