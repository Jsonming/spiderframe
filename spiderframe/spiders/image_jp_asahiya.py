# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_asahiya'
    start_urls = ["https://asahiya-jp.com/category/book/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        next_urls = response.xpath('//a[@class="nextpostslink"]/@href').extract()
        for next_url in next_urls:
            yield scrapy.Request(next_url, callback=self.parse)
        img_urls = response.xpath('//li[@class="heightLine"]/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//img[@class="attachment-post-thumbnail size-post-thumbnail wp-post-image"]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] ="image_asahiya"
        yield item
