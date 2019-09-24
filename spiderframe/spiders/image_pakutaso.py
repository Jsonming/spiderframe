# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import re
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_pakutaso'
    start_urls = ["https://www.pakutaso.com/category.html"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//li[@class="categories__item"]/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        category_url = response.url
        urls = re.split("/", category_url)
        category=urls[-2]
        img_urls = response.xpath('//article[@class="photoEntries"]/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})

    def parse_content(self, response):
        category=response.meta['category']
        img_urls = response.xpath('//*[@id="photoImage"]/@src').extract()
        item = ImgsItem()
        item["category"] =  category
        item["image_urls"] = img_urls
        yield item

