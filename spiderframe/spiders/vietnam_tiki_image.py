# -*- coding: utf-8 -*-
import json
import re

from scrapy_redis.spiders import RedisSpider

from spiderframe.items import ImgsItem


class VietnamTikiImageSpider(RedisSpider):
    name = 'vietnam_tiki_image'
    allowed_domains = ['tiki.vn']
    start_urls = [
        # 'https://tiki.vn/nhung-giac-mo-o-hieu-sach-morisaki-p614854.html?src=recently-viewed&2hi=1',
        # 'https://tiki.vn/sach-vai-counting-animal-p16580867.html?src=search&2hi=1&keyword=s%C3%A1ch'
        "https://tiki.vn/bo-62-bookmark-momoland-p14957879.html?src=search&2hi=1&keyword=s%C3%A1ch"
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
        category = re.findall(r"keyword=(.*)", response.url, re.I)
        cate = category[0] if category else "other"

        if img_url_str:
            img_url_dict = json.loads(img_url_str[0])[0]
            large_url, medium_url = img_url_dict.get("large_url"), img_url_dict.get("large_url")
            url = large_url if large_url else medium_url
            if url:
                item = ImgsItem(category=cate, image_urls=[url])
                yield item
        else:
            print("_____________" + response.url)
