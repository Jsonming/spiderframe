# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class NetherlandsNrcLinkSpider(scrapy.Spider):
    name = 'Netherlands_nrc_link'
    allowed_domains = ['www.nrc.nl/']
    start_urls = ["https://www.nrc.nl/nieuws/"]

    # start_urls = ["https://www.nrc.nl/"]
    #
    # def parse(self, response):
    #     patterns = response.xpath('//ul[@class="nav-sidebar__col__items"]/li/a/@href').extract()
    #     for pattern in patterns:
    #         if "https" not in pattern:
    #             link = "https://www.nrc.nl"+pattern
    #             yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)
    #
    # def parse_url(self, response):
    #     patterns = response.xpath('//a[@class="block__more-link"]/@href').extract()
    #     for pattern in patterns:
    #         link = "https://www.nrc.nl"+pattern
    #         yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True)
    #
    #
    # def parse_link(self, response):
    #     links = response.xpath('//a[@class="nmt-item__link"]/@href').extract()
    #     for link in links:
    #         # print(link)
    #         item = SpiderframeItem()
    #         item['url'] = link
    #         print(item)
    #         # yield item

    def start_requests(self):
        for year in range(2015,2019):
            for month in range(1,13):
                month = str(month).zfill(2)
                for day in range(1, 31):
                    day = str(day).zfill(2)
                    url = "https://www.nrc.nl/nieuws/{year}/{month}/{day}/".format(year=year,month=month,day=day)
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
    #     next_links = response.xpath('//a[@class="page-nav__button"]//@href').extract()
    #     for next_link in next_links:
    #         next_link = "https://www.nrc.nl"+next_link
    #         yield scrapy.Request(url=next_link,callback=self.parse,dont_filter=True)

        links = response.xpath('//a[@class="nmt-item__link"]//@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = "https://www.nrc.nl"+link
            # print(item)
            yield item


