# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class UnitedArabEmiratesAlbayanLinkSpider(scrapy.Spider):
    name = 'UnitedArabEmirates_albayan_link'
    allowed_domains = ['www.albayan.ae/']
    start_urls = ["https://www.albayan.ae/"]

    def parse(self, response):
        patterns = response.xpath('//section[@class="row"]//ul[@class="menu"]/li//a/@href').extract()
        for pattern in patterns:
            if "https://" not in pattern and "javascript:void(0)" not in pattern:
                link = "https://www.albayan.ae"+pattern
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)
            elif "javascript:void(0)" not in pattern:
                yield scrapy.Request(url=pattern, callback=self.parse_url, dont_filter=True)


    def parse_url(self, response):
        # print(response.url)
        links = response.xpath('//h3/a/@href').extract()
        for link in links:
            link="https://www.albayan.ae"+link
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item


