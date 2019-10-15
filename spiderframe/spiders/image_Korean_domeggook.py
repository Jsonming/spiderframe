# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_domeggook'
    start_urls = ["http://domeggook.com/main/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//li[@class="mainCate"]/a/@href').extract()
        for img_url in img_urls:
            img_url="http://domeggook.com"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//ul[@class="subcate"]//a/@href').extract()
        for img_url in img_urls:
            img_url="http://domeggook.com"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_img, dont_filter=True)

    def parse_img(self, response):
        category = response.xpath('//li[@id="lPathCat2"]//text()').extract()
        next_urls = response.xpath('//a[@class="bgYUI next"]/a/@href').extract()
        for next_url in next_urls:
            yield scrapy.Request(next_url, callback=self.parse_img)
        img_urls = response.xpath('//ol[@class="lItemList"]/li/a/@href').extract()
        for img_url in img_urls:
            img_url="http://domeggook.com"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})


    def parse_content(self, response):
        category = response.meta['category']
        img_urls = response.xpath('//img[@class="mainThumb"]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        category = category[0]
        if "/" in category:
            category=re.sub("/","",category)
            item["category"] = category
        else:
            item["category"] = category
        yield item
