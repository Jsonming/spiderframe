# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_duan'
    start_urls = ["http://duan.jp"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//div[@class="categorylist"]/a/@href').extract()
        for img_url in img_urls:
            img_url="http://duan.jp"+img_url[1:]
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        category = response.xpath('//td[@class="table1meisai"]/a/text()').extract()
        img_urls = response.xpath('//td[@class="table1meisai"]/a/@href').extract()
        for img_url in img_urls:
            img_url = "http://duan.jp" + img_url[2:]
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})

    def parse_content(self, response):
        category = response.meta['category']
        img_urls = response.xpath('//td[@class="table1meisai"]/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["http://duan.jp" + img_urls[0][2:]]
        category = category[0]
        if "/" in category:
            category=re.sub("/","",category)
            item["category"] = category+"image_duan"
        else:
            item["category"] = category+"image_duan"
        yield item
