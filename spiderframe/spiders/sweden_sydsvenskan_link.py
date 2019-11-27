# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from spiderframe.items import SpiderframeItem


class SwedenSydsvenskanLinkSpider(scrapy.Spider):
    name = 'sweden_sydsvenskan_link'
    allowed_domains = ['www.sydsvenskan.se']
    start_urls=["https://www.sydsvenskan.se/"]

    def parse(self, response):
        patterns = response.xpath('//ul//li/a/@href').extract()
        for pattern in patterns:
            if "http" not in pattern:
                link = "https://www.sydsvenskan.se"+pattern
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_links = response.xpath('//a[contains(@class, "button pagination__link pagination__link")]/@href').extract()
        for next_link in next_links:
            next_link = "https://www.sydsvenskan.se" +next_link
            yield scrapy.Request(url=next_link, callback=self.parse_url, dont_filter=True)

        links = response.xpath('//a[@class=" teaser__text-link"]/@href').extract()
        for link in links:
            link = "https://www.sydsvenskan.se" +link
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item




