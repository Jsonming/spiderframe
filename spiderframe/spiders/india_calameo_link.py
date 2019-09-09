# -*- coding: utf-8 -*-
import scrapy
import re


class IndiaCalameoLinkSpider(scrapy.Spider):
    name = 'india_calameo_link'
    allowed_domains = ['en.calameo.com']
    start_urls = ['https://en.calameo.com/read/0040912082f104473a0db?page=1']

    def parse(self, response):
        img_frist = response.xpath(r'//link[@rel="image_src"]/@href').extract()[0]
        content = response.xpath(r'//meta[@name="description"]/@content').extract()[0]

        pages = re.findall("Length: (.*?)pages", content, re.I)
        print(img_frist, pages)


