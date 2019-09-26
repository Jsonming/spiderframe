# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import re
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_mirror'
    start_urls = ["http://www.mirror.boredpanda.com/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//ul/li/a/@href').extract()
        for img_url in img_urls:
            urls = re.split("/", img_url)
            if len(urls)==5:
                image_urls=[img_url+"page/{i}/".format(i=i) for i in range(1, 3)]
                for image_url in image_urls:
                    yield scrapy.Request(url=image_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        category_url = response.url
        urls = re.split("/", category_url)
        category=urls[-2]
        img_urls = response.xpath('//a[@class="title"]/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})

    def parse_content(self, response):
        category=response.meta['category']
        img_urls = response.xpath('//div/p//img/@src').extract()
        print(img_urls)
        item = ImgsItem()
        item["category"] =  category
        item["image_urls"] = img_urls
        yield item

