# -*- coding: utf-8 -*-

import scrapy

from spiderframe.items import ImgsItem
import demjson
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_unsplash'

    def __init__(self, category="sky", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 3):
            url = "https://unsplash.com/napi/search/photos?query={category}&xp=&per_page=20&page={i}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.text
        json_contents = demjson.decode(page)
        for json_content in json_contents["results"]:
            urls = json_content["urls"]
            image=urls["raw"]
            item = ImgsItem()
            item["category"] = self.category
            item["image_urls"] = [image]
            yield item
