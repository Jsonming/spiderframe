# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import re
from urllib.parse import quote

class ImageSpider(scrapy.Spider):
    name = 'image_photock'

    def __init__(self, category="天空", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 3):
            url = "https://www.photock.jp/list/s/search/{i}/?name={category}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        next_urls = response.xpath('/html/body/div/section/div[2]/div[1]/ul[2]/li[8]/a/@href').extract()
        for next_url in next_urls:
            next_url="https://www.photock.jp"+next_url
            yield scrapy.Request(next_url, callback=self.parse)
        img_urls = response.xpath('//dd[@class="title"]/a/@href').extract()
        for img_url in img_urls:
            img_url="https://www.photock.jp"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//h2/a/img/@src').extract()
        item = ImgsItem()
        item["category"] =  self.category
        item["image_urls"] = ["https://www.photock.jp"+img_urls[0]]
        yield item

