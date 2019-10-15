# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import SpiderframeItem


class HebrewWallaLinkSpider(scrapy.Spider):
    name = 'hebrew_walla_link'
    allowed_domains = ['www.walla.co.il']
    start_urls = [
        # 'https://news.walla.co.il/category/{}'.format(i) for i in range(20, 30)
        'https://news.walla.co.il/archive/{}?month={}&year={}'.format(i, m, y) for i in range(30, 50) for m in
        range(1, 13) for y in range(2006, 2020)
    ]

    def parse(self, response):
        links = response.xpath("//section[(contains(@class, 'sequence'))]//a/@href").extract()
        for url in links:
            item = SpiderframeItem()
            item['url'] = url
            yield item
