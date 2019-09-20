# -*- coding: utf-8 -*-

import scrapy
import re
from spiderframe.items import ImgsItem
import demjson
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_pexels'

    def __init__(self, category="冰雕", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 3):
            url = "https://www.pexels.com/zh-cn/search/{category}/?format=js&seed=2019-09-20%2B02%3A30%3A53%2B%2B0000&page={i}&type=".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.text
        pattern=re.findall(r"data-photo-modal-image-download-link=\\'(https://images.pexels.com/photos/.*?\.jpg&amp;fm=jpg)\\",page)
        item = ImgsItem()
        item["category"] = self.category
        item["image_urls"] = pattern
        yield item
