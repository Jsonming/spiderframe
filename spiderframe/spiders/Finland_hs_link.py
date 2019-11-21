# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class FinlandHsLinkSpider(scrapy.Spider):
    name = 'Finland_hs_link'
    allowed_domains = ['www.hs.fi/']
    start_urls=["https://www.hs.fi/"]

    def parse(self, response):
        patterns = response.xpath('//a[@class="0"]/@href').extract()
        for pattern in patterns:
            # print(pattern)
            link="https://www.hs.fi"+pattern
            yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        data_id = response.xpath('//div[@class="is-more-items"]/a/@data-id').extract()
        data_froms = response.xpath('//div[@class="is-more-items"]/a/@data-from').extract()
        pageId = response.xpath('//body/@data-page-id').extract()
        print(data_id,data_froms,pageId)
        if data_id and data_froms:
            data_froms = int(data_froms[0])
            for data_from in range(data_froms,500,data_froms):
                link = "https://www.hs.fi/rest/laneitems/{data_id}/moreItems?from={data_from}&pageId={pageId}&even=false".format(data_id=data_id[0],data_from=data_from,pageId=pageId[0])
                yield scrapy.Request(url=link, callback=self.parse_link, dont_filter=True)

    def parse_link(self, response):
        links = response.xpath('//article/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = "https://www.hs.fi"+link
            # print(item)
            yield item


