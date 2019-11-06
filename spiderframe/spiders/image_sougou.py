# -*- coding: utf-8 -*-
from urllib.parse import quote

import demjson
import scrapy

from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_sougou'

    def __init__(self, category="", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category


    def start_requests(self):
        for j in range(0, 816, 48):
            for mode in [2,3]:
                # url = "https://pic.sogou.com/pics?query={category}&st=255&mode=255&start={j}&reqType=ajax&reqFrom=result&tn=0".format(
                #     category=quote(self.category), j=j)
                url = "https://pic.sogou.com/pics?query={category}&st=255&mode={mode}&mood=0&dm=0&start={j}&reqType=ajax&reqFrom=result&tn=0".format(
                    category=quote(self.category),mode=mode, j=j) #中
                # url = "https://pic.sogou.com/pics?query={category}&st=255&mode=2&mood=0&dm=0&start={j}&reqType=ajax&reqFrom=result&tn=0".format(
                #     category=quote(self.category), j=j) #大
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        category=response.meta['category']
        resp = demjson.decode(response.text)
        data = resp.get("items", [])
        for img in data:
            pic_url = img.get("pic_url")
            item = ImgsItem()
            item["category"] = category
            item["image_urls"] = [pic_url]
            yield item

