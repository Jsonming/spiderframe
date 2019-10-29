# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem

class ImageSpider(scrapy.Spider):
    name = 'image_morinaga'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in range(1,6):
            for j in range(1, 6):
                url="https://www.morinaga.co.jp/products/list.php?id=0{i}0{j}".format(i=i,j=j)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        img_urls = response.xpath('//li[@class="products__list__item is-new"]/a/@href').extract()
        for img_url in img_urls:
            img_url = "https://www.morinaga.co.jp/products/" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//div[@class="products-mainImg is-new"]/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = ["https://www.morinaga.co.jp"+img_urls[0]]
        item["category"] = "image_morinaga"
        yield item
