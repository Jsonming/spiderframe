# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_ajinomoto'
    start_urls = ["https://www.ajinomoto.co.jp/products/?t=search-by-category#cate00"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//div[@class="body"]/ul/li/a/@href').extract()
        for img_url in img_urls:
            img_url="https://www.ajinomoto.co.jp"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)


    def parse_content(self, response):
        img_urls = response.xpath('//div[@class="productWrap"]/p/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["https://www.ajinomoto.co.jp/"+img_urls[0]]
        item["category"] = "image_ajinomoto"
        yield item
