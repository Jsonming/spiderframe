# -*- coding: utf-8 -*-
import scrapy


class HebrewWallaLinkSpider(scrapy.Spider):
    name = 'hebrew_walla_link'
    allowed_domains = ['www.walla.co.il']
    start_urls = [
        # 'https://news.walla.co.il/category/18',
        'https://news.walla.co.il/archive/18?month=11&year=2018'
    ]

    def parse(self, response):
        links = response.xpath("//section[(contains(@class, 'sequence'))]//a/@href").extract()
        print(links)
