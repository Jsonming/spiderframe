# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class NorwayDagbladetLinkSpider(scrapy.Spider):
    name = 'Norway_dagbladet_link'
    allowed_domains = ['https://www.dagbladet.no/']
    start_urls = ["https://www.dagbladet.no/"]

    def parse(self, response):
        links = response.xpath('//nav//ul//li//a/@href').extract()
        for link in links:
            if "www" in link:
                link="https:"+link
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//article/a//@href').extract()
        for link in links:
            if "https://" in link:
                item = SpiderframeItem()
                item['url'] = link
                yield item


