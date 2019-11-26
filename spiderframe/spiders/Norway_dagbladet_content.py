# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class NorwayDagbladetContentSpider(RedisSpider):
    name = 'Norway_dagbladet_content'
    allowed_domains = ['www.dagbladet.no']
    # start_urls = ['https://www.dagbladet.no/nyheter/politiets-skrekktall---helt-sjukt/71812219']

    # redis_key = 'Norway_dagbladet_link'
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
            sql = "select url from Norway_dagbladet_content1;"
            cursor.execute(sql)
            while True:
                conn.ping()
                result = cursor.fetchone()
                if result:
                    url = result[0]
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        title = response.xpath('//h2/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = content.replace("\n", "  ")
        content = content.replace("\t", "  ")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        # print(item)
        yield item

