# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider

from spiderframe.download import you_get_download


class VideoBaseSpider(RedisSpider):
    name = 'video_base'
    redis_key = 'video_bilibili_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        you_get_download(response.url, rename=True)
