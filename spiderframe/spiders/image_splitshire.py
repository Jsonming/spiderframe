# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import re
from urllib.parse import quote

class ImageSpider(scrapy.Spider):
    name = 'image_splitshire'

    def __init__(self, category="sky", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 3):
            url = "https://www.splitshire.com/page/{i}/?s={category}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        next_urls = response.xpath('//a[@class="btn btn-link text-default-color btn-icon-right"]/@href').extract()
        for next_url in next_urls:
            yield scrapy.Request(next_url, callback=self.parse)
        img_urls = response.xpath('//div[@class="t-entry-visual-cont"]/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//div[@id="featured-img-id"]/img/@src').extract()
        item = ImgsItem()
        item["category"] =  self.category
        item["image_urls"] = img_urls
        yield item


