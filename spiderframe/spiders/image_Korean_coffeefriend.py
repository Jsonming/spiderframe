# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_coffeefriend'
    start_urls = ["http://coffeefriend.co.kr/"]


    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//div[@class="postion"]/ul/li/a/@href').extract()
        for img_url in img_urls:
            img_url="http://coffeefriend.co.kr"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True,meta={"category_url":img_url})

    def parse_url(self, response):
        category_url = response.meta['category_url']
        category = response.xpath('//*[@id="contents"]/div[1]/h2/span/text()').extract()
        next_urls = response.xpath('//*[@id="contents"]/div[3]/div[3]/p[3]/a/@href').extract()
        for next_url in next_urls:
            next_url=category_url+next_url
            yield scrapy.Request(next_url, callback=self.parse_url,meta={"category_url":category_url})
        img_urls = response.xpath('//a[@class="prdImg"]/@href').extract()
        for img_url in img_urls:
            img_url = "http://coffeefriend.co.kr" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={"category":category})

    def parse_content(self, response):
        category = response.meta['category']
        img_urls = response.xpath('//img[@class="BigImage "]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["http:"+img_urls[0]]
        category = category[0]
        if "/" in category:
            category=re.sub("/","",category)
            item["category"] = category+"image_coffeefriend"
        else:
            item["category"] = category+"image_coffeefriend"
        yield item
