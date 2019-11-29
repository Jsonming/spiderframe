# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class FinlandTsLinkSpider(scrapy.Spider):
    name = 'Finland_ts_link'
    allowed_domains = ['www.ts.fi/']
    start_urls=["https://www.ts.fi/"]

    def parse(self, response):
        patterns = response.xpath('//ul[@class="c-helper-menu c-helper-menu--level-0"]/li/a/@href').extract()
        for pattern in patterns:
            if "http" not in pattern:
                link = "https://www.ts.fi"+pattern
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_urls = response.xpath('//a[contains(@class, "c-helper-pager__item__link c-helper-pager__item__link--active")]/@href').extract()
        for next_url in next_urls:
            link = "https://www.ts.fi" + next_url
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

        links = response.xpath('//div[contains(@class,"tsv3-c-common-elementcollection__element")]/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = "https://www.ts.fi"+link
            # print(item)
            yield item
