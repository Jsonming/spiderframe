# -*- coding: utf-8 -*-
from urllib.parse import quote


import scrapy
import demjson
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_360'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = "大雾天汽车"


    def start_requests(self):
        categorys = [
            "大雾天汽车图片",
            "大雾汽车",
            "大雾天气汽车",
            "大雾天气汽车图片",
            "大雾天交通",
            "大雾天交通图片",
            "大雾高速路",
            "大雾高速堵车",
            "大雾高速堵车照片",
            "大雾天气行车",
            "汽车大雾天气",

        ]
        for category in categorys:
            for j in range(130, 870, 60):
                for zoom in [1,2]:
                    url = "https://image.so.com/j?q={category}&src=srp&correct={category}&pn=60&ch=&sn={j}&ps={i}&pc=59&pd=1&prevsn=0" \
                          "&sid=158006fec602594e0ce27b7f60615954&ran=0&ras=0&cn=0&gn=0&kn=0&comm=1&z=1&i=0&cmg=f127e4b231fc8a3e79524d70e5e44247&" \
                          "zoom={zoom}".format(category=quote(category), j=j, i=j - 6, zoom=zoom)
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

