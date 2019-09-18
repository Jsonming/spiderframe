# -*- coding: utf-8 -*-
from urllib.parse import quote

import demjson
import scrapy

from spiderframe.items import SpiderframeItem


class ImageSpider(scrapy.Spider):
    name = 'video_skypixel_link'

    def __init__(self, category="门", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 20, 20):
            url = "https://www.skypixel.com/api/v2/searches/videos?lang=zh-Hans&platform=web&device=desktop" \
                  "&keyword={category}&limit=20&offset={i}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.text
        json_content = demjson.decode(page)
        json_contents = json_content["data"]
        for json_list in json_contents["items"]:
            slug = json_list.get("slug")
            url = "https://www.skypixel.com/api/v2/videos/" + slug + "?lang=zh-Hans&platform=web&device=desktop"
            yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        page = response.text
        json_content = demjson.decode(page)
        json_contents = json_content["data"]
        json_list = json_contents["item"]
        cdn_url = json_list.get("cdn_url")
        large_mp4 = cdn_url.get("large")
        item = SpiderframeItem()
        item["url"] = large_mp4
        yield item
