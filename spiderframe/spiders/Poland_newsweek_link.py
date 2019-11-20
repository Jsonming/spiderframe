# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class PolandNewsweekLinkSpider(scrapy.Spider):
    name = 'Poland_newsweek_link'
    allowed_domains = ['www.newsweek.pl/']
    start_urls = ["https://www.newsweek.pl/"]

    def parse(self, response):
        patterns = response.xpath('//nav//ul/li//a/@href').extract()
        for pattern in patterns:
            for i in range(0,10):
                link = "https://www.newsweek.pl{pattern}?ajax=1&page={i}".format(pattern=pattern,i=i)
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//a[@class="elemRelative"]/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item


