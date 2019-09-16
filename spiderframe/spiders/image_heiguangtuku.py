# -*- coding: utf-8 -*-
import time
from urllib.parse import quote

import scrapy
from lxml import etree

from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_heiguang'

    def __init__(self, category="新生儿", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for j in range(0, 1200):
            url = "https://tu.heiguang.com/search/works?wd={category}&page={j}".format(category=quote(self.category),
                                                                                       j=j)  # 黑光
            time.sleep(3)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # 黑光
        resp = response.text
        time.sleep(3)
        html = etree.HTML(resp)
        img_urls = html.xpath('//a[@class="W-img rel"]/@href')

        for img_url in img_urls:
            true_url = "https://tu.heiguang.com" + img_url
            yield scrapy.Request(url=true_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        resp = response.text
        time.sleep(3)
        html = etree.HTML(resp)
        img_urls = html.xpath('//div[@class="show-img-item"]/img/@src')
        img_name = html.xpath('//div[@class="show-img-item"]/img/@alt')[0]
        print(img_name)
        for img_url in img_urls:
            item = ImgsItem()
            item["category"] = img_name
            item["image_urls"] = [img_url]
            yield item
