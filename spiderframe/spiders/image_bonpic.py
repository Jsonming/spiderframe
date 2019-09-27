# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import re
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_bonpic'
    start_urls = ["https://bonpic.com/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//a[@class="m"]/@href').extract()
        for img_url in img_urls:
            img_url="https://bonpic.com"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_urls = response.xpath('//div[@class="paginator"]/ul/li[last()]/a/@href').extract()
        for next_url in next_urls:
            next_url="https://bonpic.com"+next_url
            yield scrapy.Request(next_url, callback=self.parse_url)
        category_url = response.url
        urls = re.split("/", category_url)
        category=urls[-3]
        img_urls = response.xpath('//div[@class="wpmini"]/a/@href').extract()
        for img_url in img_urls:
            img_url = "https://bonpic.com" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})

    def parse_content(self, response):
        category=response.meta['category']
        img_urls = response.xpath('//a[@class="img"]/img/@src').extract()
        item = ImgsItem()
        item["category"] =  category
        item["image_urls"] = ["https://bonpic.com"+img_urls[0]]
        yield item

