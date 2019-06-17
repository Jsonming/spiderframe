# -*- coding: utf-8 -*-
import scrapy


class VietnamNewsVnLinkSpider(scrapy.Spider):
    name = 'vietnam_news_vn_link'
    allowed_domains = ['https://vnexpress.net/thoi-su']
    start_urls = ['https://vnexpress.net/thoi-su']

    def parse(self, response):
        links = response.xpath('/html/body/section[2]/section[1]/article/h4/a[1]/@href').extract()
        print(links)
