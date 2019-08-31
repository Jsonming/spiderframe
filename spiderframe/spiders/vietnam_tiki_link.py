# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class VietnamTikiLinkSpider(scrapy.Spider):
    name = 'vietnam_tiki_link'
    allowed_domains = ['tiki.vn']
    start_urls = ['https://tiki.vn/search?q=sách&ref=searchBar&page={}'.format(i) for i in range(30, 35)]

    def parse(self, response):
        urls = response.xpath('//div[@class="product-box-list"]/div/a/@href').extract()
        for url in urls:
            item = SpiderframeItem()
            item['url'] = url
            item['ori_url'] = response.url
            yield item
