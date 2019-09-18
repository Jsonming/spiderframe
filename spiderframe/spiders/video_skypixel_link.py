# -*- coding: utf-8 -*-
import demjson
import scrapy

from spiderframe.items import SpiderframeItem


class ImageSpider(scrapy.Spider):
    name = 'video_skypixel_link'

    def start_requests(self):
        for i in range(0, 40, 20):
            url = "https://www.skypixel.com/api/v2/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&" \
                  "filter=featured:true&limit=20&offset={}".format(i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.text
        json_content = demjson.decode(page)
        json_contents = json_content["data"]
        for json_list in json_contents["items"]:
            cdn_url = json_list.get("cdn_url")
            if type(cdn_url) == dict:
                large_mp4 = cdn_url.get("large")
                item = SpiderframeItem()
                item["url"] = large_mp4
                yield item
            else:
                print("error: ")
