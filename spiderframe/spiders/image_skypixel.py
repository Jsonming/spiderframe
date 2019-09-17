# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import ImgsItem
import demjson
import sys
import imp
imp.reload(sys)

class ImageSpider(scrapy.Spider):
    name = 'image_skypixel'

    def start_requests(self):
        for i in range(0, 20, 20):
            url="https://www.skypixel.com/api/v2/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&filter=featured:true&limit=20&offset={}".format(i)
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
            item["image_urls"] = large_image
            yield item
