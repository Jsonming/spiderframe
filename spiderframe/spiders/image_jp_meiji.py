# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_meiji'
    start_urls = ["https://www.meiji.co.jp/products/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//div[@class="submenu-area"]/ul/li/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_patterns = response.xpath('//li[@class="row"]/p/a[1]/@href').extract()
        for img_pattern in img_patterns:
            pattern=re.findall("\d\/(.*?)\.html",img_pattern)
            img_url="https://catalog-p.meiji.co.jp/imageDisp.php?type=product&id={}".format(pattern[0])
            item = ImgsItem()
            item["image_urls"] = [img_url]
            item["category"] = "image_meiji"
            yield item
