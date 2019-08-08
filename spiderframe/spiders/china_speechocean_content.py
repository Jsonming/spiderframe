# -*- coding: utf-8 -*-
import scrapy


class ChinaSpeechoceanContentSpider(scrapy.Spider):
    name = 'china_speechocean_content'
    allowed_domains = ['www.speechocean.com']
    start_urls = ['http://www.speechocean.com/']

    def parse(self, response):
        products = response.xpath('//div[@class="tit-list"]/div')
        for product in products:
            print(product)
