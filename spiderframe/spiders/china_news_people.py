# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from urllib import parse
from ..items import SpiderframeItem


class ChinaNewsPeopleSpider(scrapy.Spider):
    name = 'china_news_people_link'
    allowed_domains = ['www.people.com.cn']
    start_urls = [
        # 'http://news.people.com.cn/',
        "http://www.people.com.cn/GB/59476/review/{}.html".format((datetime.datetime.today() + datetime.timedelta(days=-i)).strftime("%Y%m%d")) for i in range(0, 6 * 365)

    ]

    def parse(self, response):
        # data = json.loads(response.text)
        # items = data.get("items")
        # for item in items:
        #     url = item.get("url")
        #     item = SpiderframeItem()
        #     item['url'] = url
        #     yield item

        # links = response.xpath('//div[@class="hdNews clearfix"]//a/@href').extract()
        # links = response.xpath('//ul[@class="list_14b"]//a/@href').extract()
        # links = response.xpath('//ul[@class=" list_16 mt10"]//a/@href').extract()
        # links = response.xpath('//dl[@class="list_14"]//a/@href').extract()
        # links = response.xpath('//ul[@class="list_14 mt15"]//a/@href').extract()
        # next_page = response.xpath('//*[@id="p2Ab_1"]/div[13]/a[last()]/@href').extract_first()
        # next_page = response.xpath('//div[@class="page"]/a[last()]/@href').extract_first()
        # next_page = response.xpath('//div[@class="page_n clearfix"]/a[last()]/@href').extract_first()
        # param = response.url.split('/')[-1]
        # next_page_url = response.url.replace(param, '') + next_page
        # yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)

        links = response.xpath('//td[@class="p6"]/a/@href').extract()
        for url in links:
            item = SpiderframeItem()
            item['url'] = url.strip()
            yield item