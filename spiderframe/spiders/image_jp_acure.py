# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_acure'
    start_urls = ["https://ec.shop.acure-fun.net/GoodsList.jsp"]


    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        next_urls = response.xpath('//a[@class="PAGING_LINK"]/@href').extract()
        for next_url in next_urls:
            next_url="https://ec.shop.acure-fun.net/"+next_url
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
        img_urls = response.xpath('//a[@class="goodsName"]/@href').extract()
        for img_url in img_urls:
            img_url="https://ec.shop.acure-fun.net"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//ul[@class="p-slider__nav"]/li/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["https://ec.shop.acure-fun.net"+img_urls[0]]
        item["category"] = "image_acure"
        yield item
