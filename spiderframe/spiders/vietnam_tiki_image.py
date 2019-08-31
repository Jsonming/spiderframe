# -*- coding: utf-8 -*-
import scrapy
import re
import json
from spiderframe.items import ImgsItem
from scrapy_redis.spiders import RedisSpider


class VietnamTikiImageSpider(RedisSpider):
    name = 'vietnam_tiki_image'
    allowed_domains = ['tiki.vn']
    start_urls = [
        # 'https://tiki.vn/nhung-giac-mo-o-hieu-sach-morisaki-p614854.html?src=recently-viewed&2hi=1',
        'https://tiki.vn/sach-vai-counting-animal-p16580867.html?src=search&2hi=1&keyword=s%C3%A1ch'
    ]

    redis_key = 'vietnam_tiki_link'
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        resp = response.text
        img_url_str = re.findall(r" var images = (.*?);", resp, re.I)
        if img_url_str:
            img_url_dict = json.loads(img_url_str[0])[0]
            large_url, medium_url = img_url_dict.get("large_url"), img_url_dict.get("large_url")
            url = large_url if large_url else medium_url
            if url:
                item = ImgsItem(category="vietnam", image_urls=[url])
                yield item
        else:
            print("_____________" + response.url)
