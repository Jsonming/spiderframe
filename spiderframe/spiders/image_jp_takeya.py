# -*- coding: utf-8 -*-
import scrapy
import re
import demjson
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_takeya'
    start_urls = ["https://cn.takeya.co.jp"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//a[@class="nav-top-title"]/@href').extract()
        for img_url in img_urls:
            pattern=re.findall(r"\/category(\/.*?)\.html",img_url)
            if pattern:
                cid=pattern[0].replace("/6","5")
                urls=["https://cn.takeya.co.jp/queryapi/lists?page={i}&cid={cid}&sort=top".format(i=i,cid=cid)for i in range(1,3)]
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        resp = demjson.decode(response.text)
        data = resp.get("results", [])
        for img in data:
            img = img.get("image_url")
            item = ImgsItem()
            item["category"] = "image_takeya"
            item["image_urls"] = [img]
            yield item




