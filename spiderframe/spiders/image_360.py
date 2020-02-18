# -*- coding: utf-8 -*-
from urllib.parse import quote


import scrapy

from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_360'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        # self.category = category


    def start_requests(self):
        for j in range(130, 870, 60):
            for zoom in [1,2]:
                url = "https://image.so.com/j?q={category}&src=srp&correct={category}&pn=60&ch=&sn={j}&ps={i}&pc=59&pd=1&prevsn=0" \
                      "&sid=158006fec602594e0ce27b7f60615954&ran=0&ras=0&cn=0&gn=0&kn=0&comm=1&z=1&i=0&cmg=f127e4b231fc8a3e79524d70e5e44247&" \
                      "zoom={zoom}".format(category=quote(self.category), j=j, i=j - 6,zoom=zoom)
                      #1大尺寸 ， 2 中尺寸

                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp = demjson.decode(response.text)
        data = resp.get("list", [])
        for img in data:
            img = img.get("img")
            item = ImgsItem()
            item["category"] = self.category
            item["image_urls"] = [img]
            yield item

