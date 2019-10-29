# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_japantrendshop'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for j in range(0, 6,):
            url = "https://www.japantrendshop.com/food-drinks-c-48.html?page={j}&sort=products_sort_order".format(j=j)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        img_urls = response.xpath('//div[@class="product-description-link"]/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//a[@class="product-info-zoom"]/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] = "image_japantrendshop"
        yield item


