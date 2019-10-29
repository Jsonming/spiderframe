# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_kagome'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        start_urls = ["https://www.kagome.co.jp/products/drink/",
                      "https://www.kagome.co.jp/products/new/",
                      "https://www.kagome.co.jp/products/food/",
                      ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        img_urls = response.xpath('//p[@class="imgPart"]/img/@src').extract()
        for img_url in img_urls:
            img_url="https://www.kagome.co.jp"+img_url
            item = ImgsItem()
            item["image_urls"] = [img_url]
            item["category"] = "image_kagome"
            yield item
