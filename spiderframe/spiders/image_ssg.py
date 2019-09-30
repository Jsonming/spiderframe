"http://www.ssg.com/disp/category.ssg?ctgId=6000054786"
# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import quote
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_ssg'
    start_urls = ["http://www.ssg.com"]

    def __init__(self, category="간식", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(1, 5):
            url = "http://www.ssg.com/search.ssg?target=all&query={category}&page={i}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        ctgIds = response.xpath('//div[@class="thmb"]/a[@class="clickable"]/@href').extract()
        for ctgId in ctgIds:
            url = "http://www.ssg.com/"+ctgId
            yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//img[@id="mainImg"]/@src').extract()
        img_url="http:"+img_urls[0]
        item = ImgsItem()
        item["image_urls"] = [img_url]
        item["category"] = self.category
        yield item
