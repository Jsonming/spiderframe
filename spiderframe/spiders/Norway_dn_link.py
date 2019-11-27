# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from spiderframe.items import SpiderframeItem


class NorwayDnLinkSpider(scrapy.Spider):
    name = 'Norway_dn_link'
    allowed_domains = ['www.dn.no']
    start_urls=["https://www.dn.no/"]

    def parse(self, response):
        patterns = response.xpath('//div[@class="flyout-content__sections"]//ul//li//a/@href').extract()
        for link in patterns:
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)


    def parse_url(self, response):
        links = response.xpath('//a[contains(@class, "dre-item__title")]/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item

