# -*- coding: utf-8 -*-

import scrapy

from spiderframe.items import ImgsItem
import demjson
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_skypixel'

    def __init__(self, category="山", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 40, 20):
            url = "https://www.skypixel.com/api/v2/searches/videos?lang=zh-Hans&platform=web&device=desktop" \
                  "&keyword={category}&limit=20&offset={i}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.text
        json_content = demjson.decode(page)
        json_contents = json_content["data"]
        for json in json_contents["items"]:
            image = json["image"]
            large_image = [image["large"]]
            large_image.extend([image["medium"]])
            item = ImgsItem()
            item["category"] = self.category
            item["image_urls"] = large_image
            yield item
