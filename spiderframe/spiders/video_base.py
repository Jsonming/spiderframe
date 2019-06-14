# -*- coding: utf-8 -*-
from spiderframe.download import you_get_download
from scrapy_redis.spiders import RedisSpider


class VideoBaseSpider(RedisSpider):
    name = 'video_base'
    redis_key = 'video_bilibili_dajia_link'
    custom_settings = {
        # 指定redis数据库的连接参数
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        # 指定 redis链接密码，和使用哪一个数据库
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def parse(self, response):
        you_get_download(response.url)
