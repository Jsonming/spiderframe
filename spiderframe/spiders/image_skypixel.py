# -*- coding: utf-8 -*-
import imp
import sys

import demjson
import scrapy

from spiderframe.items import ImgsItem
<<<<<<< HEAD
import demjson
from urllib.parse import quote
import sys
import imp
=======

>>>>>>> fd5c2abe4a1ceebf7f1364d8668a46caf7e6a47d
imp.reload(sys)


class ImageSpider(scrapy.Spider):
    name = 'image_skypixel'

    def __init__(self, category="门", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 20, 20):
<<<<<<< HEAD
            url="https://www.skypixel.com/api/v2/searches/videos?lang=zh-Hans&platform=web&device=desktop&keyword={category}&limit=20&offset={i}".format(category=quote(self.category), i=i)
=======
            url = "https://www.skypixel.com/api/v2/works?lang=zh-Hans&platform=web&device=desktop&sort=hot" \
                  "&filter=featured:true&limit=20&offset={}".format(i)
>>>>>>> fd5c2abe4a1ceebf7f1364d8668a46caf7e6a47d
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
