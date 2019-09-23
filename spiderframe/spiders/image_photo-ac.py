# -*- coding: utf-8 -*-

import scrapy

from spiderframe.items import ImgsItem
import demjson
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_photo'

    def __init__(self, category="sky", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for i in range(0, 3):
            url = "https://data.api.photo-ac.com/data/search?category_id=&excludeCategory_id=&excludeKeyword=+%E4%BB%A4%E5%92%8C&keyword={category}&per_page=100&page={i}&order_by=popular&is_tag=true&language=zh-tw&token=&excludeCategoriesId=&categoriesId=&max_results=100&rate=0.56&rand=true&pow=1.678&param=14000&p5=0.9&service_type=photo_ac&lang=en&disp_language=en&overseas=true&site=1".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.text
        json_contents = demjson.decode(page)
        for json_content in json_contents["collection"]:
            image = json_content["thumbnail"]
            item = ImgsItem()
            item["category"] = self.category
            item["image_urls"] = [image]
            yield item
