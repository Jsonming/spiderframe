# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from spiderframe.items import SpiderframeItem


class NorwayAftenpostenLinkSpider(scrapy.Spider):
    name = 'Norway_aftenposten_link'
    allowed_domains = ['www.aftenposten.no']
    start_urls=["https://www.aftenposten.no/"]

    def parse(self, response):
        patterns = response.xpath('//nav/ul/li/a/@href').extract()
        for pattern in patterns:
            link = "https:"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//ul[@class="ch-subsections"]/li/a/@href').extract()
        for link in links:
            if "http" in link:
                yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True)
            else:
                link = "https:" +link
                yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True)

    def parse_link(self, response):
        links = response.xpath('//a[contains(@class, "url track-click")]/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item

