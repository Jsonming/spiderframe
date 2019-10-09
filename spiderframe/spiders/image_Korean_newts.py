# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_newts'
    start_urls = ["http://www.newts.co.kr/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//li[@class="xans-record-"]/a/@href').extract()
        for img_url in img_urls:
            img_url="http://www.newts.co.kr"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        category = response.xpath('//h2//text()').extract()
        next_urls = response.xpath('//*[@id="contents"]/div[3]/p[3]/a/@href').extract()
        for next_url in next_urls:
            next_url="http://www.newts.co.kr/product/list.html"+next_url
            yield scrapy.Request(next_url, callback=self.parse_url)
        img_urls = response.xpath('//p[@class="name"]//a/@href').extract()
        for img_url in img_urls:
            img_url = "http://www.newts.co.kr" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})

    def parse_content(self, response):
        category = response.meta['category']
        img_urls = response.xpath('//img[@class="BigImage "]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["http:"+img_urls[0]]
        item["category"] = category[0]
        yield item
