# -*- coding: utf-8 -*-
import scrapy
import json
from spiderframe.items import ImgsItem


class VietnamShopeeImageSpider(scrapy.Spider):
    name = 'vietnam_shopee_image'
    allowed_domains = ['shopee.vn']

    def __init__(self, category="sách", *args, **kwargs):
        super(VietnamShopeeImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(1, 102):
            url = "https://shopee.vn/api/v2/search_items/?by=relevancy&keyword={}&limit=50&newest={}&order=desc&page_type=search".format(self.category, i*50)
            headers = {
                'cache-control': "no-cache",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                "referer": "https://shopee.vn/search?keyword={}".format(self.category),

            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body)
        items = data.get("items")
        img_list = []
        for item in items:
            images = item.get("images")
            for img in images:
                url = "https://cf.shopee.vn/file/" + img
                img_list.append(url)

        item = ImgsItem()
        item["category"] = self.category
        item["image_urls"] = img_list
        yield item

