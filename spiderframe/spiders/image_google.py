# -*- coding: utf-8 -*-
import re
from urllib.parse import quote

import scrapy

from spiderframe.items import ImgsItem


class ImageGoogleSpider(scrapy.Spider):
    name = 'image_google'

    def __init__(self, category=None, *args, **kwargs):
        super(ImageGoogleSpider, self).__init__(*args, **kwargs)

        self.category = "大雾天气"

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
            url = 'https://www.google.com/search?ei=aM0JXfmZBcqD8gXIy7ww&yv=3&q={category}&tbm=isch&vet=10ahUKEwj57YWU7fTiAhXKgbwKHcglDwYQuT0ITCgB.aM0JXfmZBcqD8gXIy7ww.i&ved=0ahUKEwj57YWU7fTiAhXKgbwKHcglDwYQuT0ITCgB&ijn=1&start=100&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'.format(
                category=quote(category))
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        content = response.text
        pattern_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        links = re.findall(pattern_url, content)
        keyword = ["p=tbn", "images", "image", "jpg", "png", "jpeg", "PNG", "JPG", "JPEG"]
        img_urls = []
        for link in links:
            url = link.encode("utf8").decode('unicode_escape')
            is_img = any([word in url for word in keyword])
            if is_img:
                img_urls.append(url)

        item = ImgsItem()
        item["category"] = self.category
        item["image_urls"] = img_urls
        yield item

        if links:
            current_num = re.findall('&ijn=(.*?)&start=', response.url)[0]
            url = 'https://www.google.com/search?ei=aM0JXfmZBcqD8gXIy7ww&yv=3&q={category}&tbm=isch&vet=10ahUKEwj57YWU7fTiAhXKgbwKHcglDwYQuT0ITCgB.aM0JXfmZBcqD8gXIy7ww.i&ved=0ahUKEwj57YWU7fTiAhXKgbwKHcglDwYQuT0ITCgB&ijn={page}&start={page}00&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'.format(
                category=quote(self.category), page=int(current_num) + 1)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

