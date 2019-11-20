# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class TurkeyHurriyetdailynewsLinkSpider(scrapy.Spider):
    name = 'Turkey_hurriyetdailynews_link'
    allowed_domains = ['www.hurriyetdailynews.com/']
    start_urls = ["http://www.hurriyetdailynews.com/"]

    def parse(self, response):
        patterns = response.xpath('//ul[@class="nav"]/li//a/@href').extract()
        for pattern in patterns:
            link = "http://www.hurriyetdailynews.com"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//div[@class="news"]/a/@href').extract()
        for link in links:
            link = "http://www.hurriyetdailynews.com"+link
            item = SpiderframeItem()
            item['url'] = link
            yield item


