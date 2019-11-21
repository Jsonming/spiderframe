# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class GreeceTaneaLinkSpider(scrapy.Spider):
    name = 'Greece_tanea_link'
    allowed_domains = ['www.tanea.gr']
    start_urls=["https://www.tanea.gr/"]

    def parse(self, response):
        patterns = response.xpath('//h2/a/@href').extract()
        for pattern in patterns:
            link="https://www.tanea.gr"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//ul[@class="navsubmenu"]/li/a/@href').extract()
        for link in links:
            link = "https://www.tanea.gr"+link
            yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True)

    def parse_link(self, response):
        next_urls = response.xpath('//li[@class="nxtnav "]/a/href')
        for next_url in next_urls:
            yield scrapy.Request(url=next_url, callback=self.parse_link, dont_filter=True)

        links = response.xpath('//div[@class="mask-title"]/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = link
            print(item)
            # yield item


