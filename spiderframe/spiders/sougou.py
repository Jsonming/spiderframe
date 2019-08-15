# -*- coding: utf-8 -*-
import scrapy
import demjson
from spiderframe.items import ImgsItem
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_sougou'

    def __init__(self, category="做饭", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for j in range(0,816,48):
            url="https://pic.sogou.com/pics?query={category}&st=255&mode=255&start={j}&reqType=ajax&reqFrom=result&tn=0".format(category=quote(self.category),j=j)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # resp = json.loads(response.text,strict=False)
        resp = demjson.decode(response.text)
        data = resp.get("items", [])
        for img in data:
            pic_url = img.get("pic_url")
            item = ImgsItem()
            item["category"] = self.category
            item["image_urls"] = [pic_url]
            yield item

    # def parse(self, response):
    #     print('response:', response.url)
    #     item = ImgsItem()
    #     item["category"] = self.category
    #     item["image_urls"] = [response.url]
    #     yield item

