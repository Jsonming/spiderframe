# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class DenmarkJyllandsLinkSpider(scrapy.Spider):
    name = 'Denmark_jyllands_link'
    allowed_domains = ['jyllands-posten.dk']
    start_urls = ["https://jyllands-posten.dk"]

    def parse(self, response):
        patterns = response.xpath('//div[@class="siteMenuNavItem"]//a[@class="siteMenuNavItemLink"]/@href').extract()
        for link in patterns:
            # pattern=pattern.split('/')[3:]
            # print(pattern)
            # # link = "https://jyllands-posten.dk{pattern}/?widget=article&widgetId=8116054&subview=ajaxList&templateName=gridCol620&showBreaker=false&shown=12&pageSize=20".format(pattern=pattern)
            # print(link)
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//div[contains(@class, "art")]//a/@href').extract()
        for link in links:
            if "https://jyllands-posten.dk" in link:
                item = SpiderframeItem()
                item['url'] = link
                # print(item)
                yield item


