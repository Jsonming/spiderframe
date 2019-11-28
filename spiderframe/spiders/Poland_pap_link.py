# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class PolandPapLinkSpider(scrapy.Spider):
    name = 'Poland_pap_link'
    allowed_domains = ['www.pap.pl/']
    start_urls = ["https://www.pap.pl/"]

    def parse(self, response):
        patterns = response.xpath('//ul[@class="menu menu--main nav navbar-nav navigation linksList"]/li//a/@href').extract()
        for pattern in patterns:
            link = "https://www.pap.pl"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_links = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').extract()
        for next_link in next_links:
            next_link = response.url+next_link
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True)


        links = response.xpath('//div[@class="textWrapper"]/h2/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = "https://www.pap.pl"+link
            # print(item)
            yield item


