# -*- coding: utf-8 -*-
import scrapy
from spiderframe.download import you_get_download
from scrapy_redis.spiders import RedisSpider


class VideoBilibiliSpider(RedisSpider):
    name = 'video_bilibili'
    # allowed_domains = ['www.bilibili.com']
    # start_urls = ['http://www.bilibili.com/video/av7484989?from=search&seid=5659917572838529568']
    redis_key = 'video_bilibili_link'
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
