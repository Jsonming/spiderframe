# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_dccoffee'
    start_urls = ["http://www.dccoffee.co.kr/"]


    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//li[@class="xans-record-"]/a/@href').extract()
        for img_url in img_urls:
            img_url="http://www.dccoffee.co.kr"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True,meta={"category_url":img_url})

    def parse_url(self, response):
        category_url=response.meta['category_url']
        next_urls = response.xpath('//*[@id="contents"]/div[4]/p[3]/a/@href').extract()
        for next_url in next_urls:
            next_url=category_url+next_url
            yield scrapy.Request(next_url, callback=self.parse_url,meta={"category_url":category_url})
        img_urls = response.xpath('//ul[@class="prdList column4"]/li//a/@href').extract()
        for img_url in img_urls:
            img_url = "http://www.dccoffee.co.kr" + img_url
            print(img_url)
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        category = response.xpath('//*[@id="contents"]/div[1]/div/ol/li[2]/a/text()').extract()
        img_urls = response.xpath('//img[@class="BigImage "]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["http:"+img_urls[0]]
        category = category[0]
        if "/" in category:
            category=re.sub("/","",category)
            item["category"] = category+'image_dccoffee'
        else:
            item["category"] = category+'image_dccoffee'
        yield item
