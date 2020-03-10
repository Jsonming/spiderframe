# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class EgyptMasrawyContentSpider(scrapy.Spider):
    name = 'Egypt_masrawy_content'
    allowed_domains = ['www.masrawy.com']
    start_urls = [
        # 'https://www.masrawy.com/news/news_cases/details/2019/11/16/1671786/%D9%85%D9%86%D9%87%D8%A7-%D9%83%D8%B4%D9%81-%D8%BA%D9%85%D9%88%D8%B6-41-%D8%AC%D8%B1%D9%8A%D9%85%D8%A9-%D8%AA%D8%B9%D8%B1%D9%81-%D8%B9%D9%84%D9%89-%D8%AC%D9%87%D9%88%D8%AF-%D8%A7%D9%84%D8%AF%D8%A7%D8%AE%D9%84%D9%8A%D8%A9-%D8%A8%D8%A7%D9%84%D9%85%D8%AD%D8%A7%D9%81%D8%B8%D8%A7%D8%AA-%D8%AE%D9%84%D8%A7%D9%84-%D8%A3%D8%B3%D8%A8%D9%88%D8%B9'
        # "https://www.masrawy.com/news/news_cases/details/2019/11/17/1672209/%D9%83%D8%B3%D9%88%D8%B1-%D9%85%D8%B6%D8%A7%D8%B9%D9%81%D8%A9-%D9%88%D8%B5%D8%AF%D9%85%D8%A9-%D8%B9%D8%B5%D8%A8%D9%8A%D8%A9-%D9%86%D9%86%D8%B4%D8%B1-%D8%AD%D8%A7%D9%84%D8%A9-%D9%85%D8%B5%D8%A7%D8%A8%D9%8A-%D8%AD%D8%A7%D8%AF%D8%AB-%D8%A8%D8%B1%D8%AC-%D8%A3%D9%88%D8%B3%D9%8A%D9%85-"
        # "https://www.masrawy.com/news/news_cases/details/2019/11/17/1672087/%D8%B3%D9%82%D9%88%D8%B7-%D8%B9%D8%B5%D8%A7%D8%A8%D8%A9-%D8%A7%D9%84%D9%85%D8%AA%D8%A7%D8%AC%D8%B1-%D9%81%D9%8A-%D9%82%D8%A8%D8%B6%D8%A9-%D9%85%D8%A8%D8%A7%D8%AD%D8%AB-%D8%A7%D9%84%D9%85%D8%B9%D8%B5%D8%B1%D8%A9"
        # "https://www.masrawy.com/news/news_cases/details/2019/11/18/1672618/%D8%AD%D8%B1%D9%83%D8%A9-%D8%AA%D9%86%D9%82%D9%84%D8%A7%D8%AA-%D9%85%D8%AD%D8%AF%D9%88%D8%AF%D8%A9-%D8%A8%D8%A7%D9%84%D9%82%D8%A7%D9%87%D8%B1%D8%A9-%D8%A7%D9%84%D8%AC%D9%85%D9%84-%D9%84%D9%85%D8%A8%D8%A7%D8%AD%D8%AB-%D8%A7%D9%84%D8%B2%D8%A7%D9%88%D9%8A%D8%A9-%D9%88-%D8%A7%D9%84%D8%B3%D9%8A%D8%B3%D9%8A-%D9%84%D9%84%D9%86%D9%87%D8%B6%D8%A9"
        # "https://www.masrawy.com/news/news_cases/details/2019/11/8/1667160/%D8%A8%D8%B9%D8%AF-%D9%81%D9%8A%D8%AF%D9%8A%D9%88-%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D8%BA%D8%A7%D8%AB%D8%A9-%D8%B6%D8%A8%D8%B7-%D8%A8%D9%84%D8%B7%D8%AC%D9%8A%D8%A9-%D8%A8%D8%A7%D9%83%D9%88%D8%B3-%D9%81%D9%8A-%D8%A7%D9%84%D8%A5%D8%B3%D9%83%D9%86%D8%AF%D8%B1%D9%8A%D8%A9"
        # "https://www.masrawy.com/news/news_cases/details/2019/11/9/1667667/%D9%85-%D8%AF%D9%85%D9%85%D8%A9-%D9%88%D9%85%D8%AD%D8%B8%D9%88%D8%B1%D8%A9-%D8%B6%D8%A8%D8%B7-8-%D8%A3%D8%B7%D9%86%D8%A7%D9%86-%D9%86%D9%81%D8%A7%D9%8A%D8%A7%D8%AA-%D8%B7%D8%A8%D9%8A%D8%A9-%D8%AF%D8%A7%D8%AE%D9%84-%D9%85%D8%B5%D9%86%D8%B9-%D8%A8%D8%A7%D9%84%D8%AC%D9%8A%D8%B2%D8%A9-%D8%B5%D9%88%D8%B1-"
        # "https://www.masrawy.com/news/news_cases/details/2019/11/9/1667434/%D8%A8%D9%80-2-%D9%83%D9%8A%D9%84%D9%88-%D9%87%D9%8A%D8%B1%D9%88%D9%8A%D9%86-%D8%A3%D9%85%D9%86-%D8%A7%D9%84%D8%AC%D9%8A%D8%B2%D8%A9-%D9%8A%D8%B6%D8%A8%D8%B7-%D8%AA%D8%A7%D8%AC%D8%B1-%D9%85%D8%AE%D8%AF%D8%B1%D8%A7%D8%AA-%D8%A8%D8%A3%D9%88%D8%B3%D9%8A%D9%85"
        # "https://www.masrawy.com/news/news_cases/details/2019/11/10/1668055/%D9%82%D9%88%D8%A7%D9%81%D9%84-%D8%A7%D9%84%D8%AF%D8%A7%D8%AE%D9%84%D9%8A%D8%A9-%D8%AA%D8%AC%D9%88%D8%A8-8-%D9%85%D8%AD%D8%A7%D9%81%D8%B8%D8%A7%D8%AA-%D9%84%D8%AA%D9%88%D8%B2%D9%8A%D8%B9-%D8%A7%D9%84%D9%80-%D8%A8%D8%B7%D8%A7%D8%B7%D9%8A%D9%86-%D8%B9%D9%84%D9%89-%D8%A7%D9%84%D9%85%D9%88%D8%A7%D8%B7%D9%86%D9%8A%D9%86"
        "https://www.masrawy.com/news/news_cases/details/2019/11/11/1668642/%D8%A7%D9%84%D9%86%D9%82%D8%B6-%D8%AA%D9%84%D8%BA%D9%89-%D8%AA%D8%BA%D8%B1%D9%8A%D9%85-%D8%A7-%D9%84%D8%B4%D8%B1%D9%83%D8%A9-%D8%A5%D8%B9%D9%84%D8%A7%D9%85%D9%8A%D8%A9-%D9%84%D8%A7%D8%AA%D9%87%D8%A7%D9%85%D9%87%D8%A7-%D8%A8%D8%B3%D8%B1%D9%82%D8%A9-%D8%AD%D9%88%D8%A7%D8%AF%D9%8A%D8%AA-%D9%83%D8%B1%D8%AA%D9%88%D9%86%D9%8A%D8%A9-"
    ]

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
            sql = "select url from Egypt_masrawy_content limit 100;"
            cursor.execute(sql)
            for i in range(10):
                conn.ping()
                result = cursor.fetchmany(size=10)
                for item in result:
                    url = item[0]
                    # print(url)
                    yield scrapy.Request(url=url, callback=self.parse, meta={"batch": i}, dont_filter=True)

    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        contents = response.xpath('//div[@class="ArticleDetails details"]/p//text()').extract()
        print(response.meta.get("batch"))

        with open(r'D:\Workspace\spiderframe\spiderframe\files\text\{}.txt'.format(response.meta.get("batch")), 'a',
                  encoding='utf8')as f:

            for item in contents:
                f.write(item + "\n")

        # item = SpiderframeItem()
        # item['url'] = response.url
        # item['category'] = response.url.split('/')[4]
        # item['title'] = ''.join(title)
        # item['content'] = content
        # print(item)
        # yield item
