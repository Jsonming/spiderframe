# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_print365shop'
    start_urls = ["http://print365shop.cafe24.com/"]

    def parse(self, response):
        img_urls = response.xpath('//ul[@class="menu_box"]/li/a/@href').extract()
        for img_url in img_urls:
            img_url="http://print365shop.cafe24.com"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//span[@class="name"]/a/@href').extract()
        for img_url in img_urls:
            img_url = "http://print365shop.cafe24.com" + img_url
            print(img_url)
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)


    def parse_content(self, response):
        category = response.xpath('//*[@id="contents"]/div/div[1]/ol/li[2]/a//text()').extract()[0]
        img_urls = response.xpath('//img[@class="BigImage "]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["http:"+img_urls[0]]
        if "/" in category:
            category=re.sub("/","",category)
            item["category"] = category
        else:
            item["category"] = category
        yield item
