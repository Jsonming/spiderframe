# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class UnitedArabEmiratesAlkhaleejLinkSpider(scrapy.Spider):
    name = 'UnitedArabEmirates_alkhaleej_link'
    allowed_domains = ['www.alkhaleej.ae']
    start_urls = ["http://www.alkhaleej.ae/alkhaleej/localnews",
                  "http://www.alkhaleej.ae/alkhaleejnews/news",
                  "http://www.alkhaleej.ae/alkhaleejnews/education",
                  "http://www.alkhaleej.ae/alkhaleejnews/police",
                  "http://www.alkhaleej.ae/studiesandopinions/opinions",
                  "http://www.alkhaleej.ae/alkhaleej/news",
                  "http://www.alkhaleej.ae/alkhaleej/culture",
                  "http://www.alkhaleej.ae/alkhaleejnews/break",
                  "http://www.alkhaleej.ae/alkhaleejnews/magalah",
                  "http://www.alkhaleej.ae/alkhaleej/books",
                  "http://www.alkhaleej.ae/alkhaleej/file"
                  ]

    def parse(self, response):
        patterns = response.xpath('//a[@class="differentTall"]/@href').extract()
        for pattern in patterns:
            link="http://www.alkhaleej.ae"+pattern
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item


