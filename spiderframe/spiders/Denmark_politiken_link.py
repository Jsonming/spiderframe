# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class DenmarkPolitikenLinkSpider(scrapy.Spider):
    name = 'Denmark_politiken_link'
    allowed_domains = ['politiken.dk/']
    start_urls = ["https://politiken.dk/"]

    def parse(self, response):
        patterns = response.xpath('//ul[@class="topbar-nav__list js-topbar-nav__list"]/li/a/@href').extract()
        for link in patterns:
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        patterns = response.xpath('//ul[@class="topbar-nav__list js-topbar-nav__list"]/li/a/@href').extract()
        for link in patterns:
            yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True)


    def parse_link(self, response):
        links = response.xpath('//h2/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item


