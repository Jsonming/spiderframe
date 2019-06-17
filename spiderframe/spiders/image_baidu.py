# -*- coding: utf-8 -*-
import scrapy
import json


class ImageBaiduSpider(scrapy.Spider):
    name = 'image_baidu'
    allowed_domains = ['http://image.baidu.com']
    start_urls = ['http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%9A%B4%E5%8A%9B%E6%89%93%E6%9E%B6&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%E6%9A%B4%E5%8A%9B%E6%89%93%E6%9E%B6&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn=30&rn=30&gsm=1e&1560505489300=']

    def parse(self, response):
        resp = json.loads(response.text)
        data = resp.get("data", [])
        for img in data:
            thumbURL = img.get("thumbURL")
            middleURL = img.get("middleURL")
            hoverURL = img.get("hoverURL")
            objURL = img.get("objURL")
            fromURL = img.get("fromURL")

            width = img.get("width")
            height = img.get('height')


