# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class PolandNewsweekContentSpider(RedisSpider):
    name = 'Poland_newsweek_content'
    allowed_domains = ['www.newsweek.pl']
    # start_urls = ['https://www.newsweek.pl/polska/wladyslaw-kosiniak-kamysz-myla-sie-ci-ktorzy-sadza-ze-jest-prostolinijny/f75gwg6']
    #
    # redis_key = 'Poland_newsweek_link'
    #
    # custom_settings = {
    #     'REDIS_HOST': '123.56.11.156',
    #     'REDIS_PORT': 8888,
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
            sql = "select url from Poland_newsweek_content22;"
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
        content = content.replace("\n","  ")
        content = content.replace("\t","  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

