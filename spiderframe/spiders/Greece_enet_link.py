# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class GreeceEnetLinkSpider(scrapy.Spider):
    name = 'Greece_enet_link'
    allowed_domains = ['www.nrc.nl/']

    def start_requests(self):
        for year in range(2010,2019):
            for month in range(1,13):
                month = str(month).zfill(2)
                for day in range(1, 31):
                    day = str(day).zfill(2)
                    url = "http://www.enet.gr/?i=issue.el.home&date={year}-{month}-{day}".format(year=year,month=month,day=day)
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        links = response.xpath('//div[@class="box"]//ul/li//a//@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = "http://www.enet.gr/"+link
            # print(item)
            yield item


