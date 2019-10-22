# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_yamazakipan'


    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in range(1,7):
            url = "http://www.yamazakipan.co.jp/product/0{i}/index.html".format(i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        img_urls = response.xpath('//ul[@class="list-product"]/li/a/@href').extract()
        for img_url in img_urls:
            img_url="http://www.yamazakipan.co.jp"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//div[@class="img-package"]/img/@src').extract()
        item = ImgsItem()
        res_url=response.url
        pattern=re.findall(r"0\d\/(.*\.html)",res_url)
        url=res_url.replace(pattern[0],img_urls[0])
        print(url)
        item["image_urls"] = [url]
        item["category"] = "image_yamazakipan"
        yield item
