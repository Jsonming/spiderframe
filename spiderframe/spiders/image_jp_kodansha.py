# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_kodansha'
    start_urls = ["http://bookclub.kodansha.co.jp/labels"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//a[@class="list"]/@href').extract()
        for img_url in img_urls:
            if "co.jp" not in img_url:
                img_url="http://bookclub.kodansha.co.jp"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_urls = response.xpath('//a[@class="btnL_green page_scroll_nextSelector"]/@href').extract()
        for next_url in next_urls:
            next_url="http://bookclub.kodansha.co.jp"+next_url
            yield scrapy.Request(next_url, callback=self.parse_url)
        img_urls = response.xpath('//a[@class="btnDetail"]/@href').extract()
        for img_url in img_urls:
            img_url = "http://bookclub.kodansha.co.jp" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//div[@class="lineImg"]/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] = "image_kodansha"
        yield item
