# -*- coding: utf-8 -*-
import scrapy
import demjson
from spiderframe.items import ImgsItem
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_360'

    def __init__(self, category="聚餐", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for j in range(130,870,60):
            url="https://image.so.com/j?q={category}&src=srp&correct={category}&pn=60&ch=&sn={j}&ps={i}&pc=60&pd=1&prevsn=0&sid=565b6acae2affcf7b91df23eaad07a57&ran=0&ras=6&cn=0&gn=0&kn=50&comm=1&z=1&i=0&cmg=6a08b9d6079dd9a2ef67907c2fcdb344".format(category=quote(self.category),j=j,i=j-6)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # resp = json.loads(response.text,strict=False)
        resp = demjson.decode(response.text)
        data = resp.get("list", [])
        for img in data:
            img = img.get("img")
            item = ImgsItem()
            item["category"] = self.category
            item["image_urls"] = [img]
            yield item

    # def parse(self, response):
    #     print('response:', response.url)
    #     item = ImgsItem()
    #     item["category"] = self.category
    #     item["image_urls"] = [response.url]
    #     yield item

