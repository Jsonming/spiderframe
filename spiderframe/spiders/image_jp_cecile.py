# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_cecile'
    start_urls = ["https://www.cecile.co.jp/categorylist/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//ul[@class="category-list list001"]/li/h2/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_urls = response.xpath('//a[@class="sli_next_page"]/@href').extract()
        for next_url in next_urls:
            yield scrapy.Request(next_url, callback=self.parse_url)
        img_urls = response.xpath('//div[@class="itemdetail sli_list_col1"]/a/@href').extract()
        for img_url in img_urls:
            img_url = "http:" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//a[@class="modal-open"]/span/img/@src').extract()
        category = response.xpath('//*[@id="breadclumb"]/ol/li[2]/a//text()').extract()
        item = ImgsItem()
        item["image_urls"] = ["https://www.cecile.co.jp"+img_urls[0]]
        item["category"] = category[0]+'image_cecile'
        yield item
