# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class UnitedArabEmiratesAlittihadLinkSpider(scrapy.Spider):
    name = 'UnitedArabEmirates_alittihad_link'
    allowed_domains = ['www.alittihad.ae']
    start_urls = ["https://www.alittihad.ae/"]

    def parse(self, response):
        patterns = response.xpath('//ul[@class="nav navbar-nav"]//li//a/@href').extract()
        for pattern in patterns:
            patt = pattern.split("/")[2]
            if int(patt):
                for i in range(1,3):
                    link="https://www.alittihad.ae/Service/SectionNews.aspx?SectionID={patt}&pageSize=8&pageindex={i}".format(patt=patt,i=i)
                    yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//h3/a/@href').extract()
        for link in links:
            link="https://www.alittihad.ae"+link
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item


