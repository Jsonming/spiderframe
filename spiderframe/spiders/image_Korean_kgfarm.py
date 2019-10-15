# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_kgfarm'
    start_urls = ["https://kgfarm.gg.go.kr/main/main.asp"]


    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # category = response.xpath('//li[@class="xans-record-"]/a/text()').extract()
        img_urls = response.xpath('//div[@class="cate_box"]/ul/li/a/@href').extract()
        for img_url in img_urls:
            img_url="https://kgfarm.gg.go.kr"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        # next_urls = response.xpath('//*[@id="contents"]/div[4]/p[3]/a/@href').extract()
        # for next_url in next_urls:
        #     print(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse_url)
        img_urls = response.xpath('//ul[@class="listBox2"]/li/a/@href').extract()
        for img_url in img_urls:
            img_url = "https://kgfarm.gg.go.kr" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//img[@id="placeholder"]/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["https://kgfarm.gg.go.kr"+img_urls[0]]
        item["category"] = 'image_kgfarm'
        yield item
