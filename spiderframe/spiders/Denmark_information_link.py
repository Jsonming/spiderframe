# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class DenmarkInformationLinkSpider(scrapy.Spider):
    name = 'Denmark_information_link'
    allowed_domains = ['www.information.dk']

    def start_requests(self):
        for i in range(2010,2019):
            for j in range(1,12):
                url = "https://www.information.dk/arkiv/{i}-{j}".format(i=i,j=j)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        patterns = response.xpath('//div[@class="archive-front-img"]/a/@href').extract()
        for pattern in patterns:
            link = "https://www.information.dk/"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//div[@class="field field-name-field-webrubrik"]/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = "https://www.information.dk"+link
            # print(item)
            yield item


