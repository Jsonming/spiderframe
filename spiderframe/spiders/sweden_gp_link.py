# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from spiderframe.items import SpiderframeItem


class SwedenGpLinkSpider(scrapy.Spider):
    name = 'sweden_gp_link'
    allowed_domains = ['www.gp.se']
    start_urls=["https://www.gp.se"]

    def parse(self, response):
        patterns = response.xpath('//nav//ul//li/a/@href').extract()
        for pattern in patterns:
            if "http" not in pattern:
                link = "https://www.gp.se"+pattern
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)
            else:
                yield scrapy.Request(url=pattern, callback=self.parse_url, dont_filter=True)


    def parse_url(self, response):
        links = response.xpath('//a[@class="c-teaser__link"]/@href').extract()
        for link in links:
            link = "https://www.gp.se" +link
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item
