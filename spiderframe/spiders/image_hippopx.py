# -*- coding: utf-8 -*-
import json
import re
from urllib.parse import quote
from lxml import etree
import scrapy
from spiderframe.items import ImgsItem


class ImageBaiduSpider(scrapy.Spider):
    name = 'image_hippopx'

    def __init__(self, category="门", *args, **kwargs):
        super(ImageBaiduSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for j in range(0, 3):
            url = "https://www.hippopx.com/zh/search?q={category}&page={j}".format(category=quote(self.category), j=j)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp = response.text
        html = etree.HTML(resp)
        img_urls = html.xpath('//img[@itemprop="thumbnail"]/@src')
        item = ImgsItem()
        item["category"] = self.category
        item["image_urls"] = img_urls
        yield item

