# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy import FormRequest
from spiderframe.download import you_get_download


class VideoBaseSpider(RedisSpider):
    name = 'video_base'
    redis_key = 'video_bilibili_link'
    # start_urls = ["https://v.qq.com/x/cover/24bvvcald9bq5kz/p0387cjmac7.html"]

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    headers = {
        "Host": "search.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
        # "Cookie":"INTVER=1; _uuid=83B988FE-7888-58DE-B8EB-E35E0414D76E16344infoc; buvid3=B009CAB2-83B4-4166-8118-7680C3B19210155820infoc; arrange=matrix; CURRENT_FNVAL=16; LIVE_BUVID=AUTO4115754250295499; stardustvideo=1; sid=9ieqnc9g; rpdid=|(k|Y~RkY|RY0J'ul~lRk~k|~"
    }


    def make_requests_from_url(self, url):
        return FormRequest(url, dont_filter=True,headers=self.headers)

    def parse(self, response):
        # try:
        # if "/sf?pd=" not in response.url:
        you_get_download(response.url)
        # except Exception as e:
        #     with open("err.txt","w+",encoding='utf-8') as f:
        #         f.write(response.url)

