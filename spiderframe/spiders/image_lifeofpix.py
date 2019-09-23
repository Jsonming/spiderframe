# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import demjson
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_lifeofpix'

    def __init__(self, category="sky", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 3):
            url = "https://www.lifeofpix.com/search/{category}/{i}/?".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp = response.text
        html = etree.HTML(resp)
        img_urls = html.xpath('//a[@class="clickarea overlay"]/@href')
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        resp = response.text
        html = etree.HTML(resp)
        img_urls = html.xpath('//img[@id="pic"]/@src')
        item = ImgsItem()
        item["category"] =  self.category
        item["image_urls"] = img_urls
        yield item


