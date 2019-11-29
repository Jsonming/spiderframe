# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class EgyptMasrawyContentSpider(RedisSpider):
    name = 'Egypt_masrawy_content'
    allowed_domains = ['www.masrawy.com']
    # start_urls = ['https://www.masrawy.com/news/news_cases/details/2019/11/18/1672863/%D8%AA%D8%AC%D8%AF%D9%8A%D8%AF-%D8%AD%D8%A8%D8%B3-%D8%A7%D9%84%D9%85%D8%AA%D9%87%D9%85-%D9%81%D9%8A-%D8%AD%D8%A7%D8%AF%D8%AB-%D9%85%D8%B9%D9%87%D8%AF-%D8%A7%D9%84%D8%A3%D9%88%D8%B1%D8%A7%D9%85-15-%D9%8A%D9%88%D9%85%D8%A7-%D8%B9%D9%84%D9%89-%D8%B0%D9%85%D8%A9-%D8%A7%D9%84%D8%AA%D8%AD%D9%82%D9%8A%D9%82%D8%A7%D8%AA#SectionMore']
    #
    # redis_key = 'Egypt_masrawy_link'
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
            sql = "select url from Egypt_masrawy_content22;"
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
        item['category'] = response.url.split('/')[4]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

