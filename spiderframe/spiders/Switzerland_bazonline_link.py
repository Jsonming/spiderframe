# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from spiderframe.items import SpiderframeItem


class SwitzerlandBazonlineLinkSpider(scrapy.Spider):
    name = 'Switzerland_bazonline_link'
    allowed_domains = ['www.bazonline.ch/']
    start_urls=["https://www.bazonline.ch/"]

    def parse(self, response):
        patterns = response.xpath('//div[@class="menu-aa-container"]//ul//li/a/@href').extract()
        for pattern in patterns:
            link = "https://www.bazonline.ch"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//h3/a/@href').extract()
        for link in links:
            link = urllib.parse.quote(link)
            link = "https://www.tagesanzeiger.ch"+link
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item




