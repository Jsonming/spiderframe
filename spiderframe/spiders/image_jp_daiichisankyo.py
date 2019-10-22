# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_daiichisankyo'
    start_urls = ["https://www.daiichisankyo-hc.co.jp/products/brand/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//a[@class="hover-a"]/@href').extract()
        for img_url in img_urls:
            img_url="https://www.daiichisankyo-hc.co.jp"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//div[@class="mdt__item-c"]//a[@class="hover-a"]/@href').extract()
        for img_url in img_urls:
            img_url = "https://www.daiichisankyo-hc.co.jp" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        img_urls = response.xpath('//div[@class="mdt__item-a-outer"]//a[@class="hover-a"]/@href').extract()
        for img_url in img_urls:
            img_url = "https://www.daiichisankyo-hc.co.jp" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//img[@class="mdt-item-thumb__img"]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["https://www.daiichisankyo-hc.co.jp"+img_urls[0]]
        item["category"] = "image_daiichisankyo"
        yield item
