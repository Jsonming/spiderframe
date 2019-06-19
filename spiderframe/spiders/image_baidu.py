# -*- coding: utf-8 -*-
import re
import scrapy
import json
from spiderframe.items import ImgsItem
from urllib.parse import quote


class ImageBaiduSpider(scrapy.Spider):
    name = 'image_baidu'

    def __init__(self, category=None, *args, **kwargs):
        super(ImageBaiduSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={category}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={category}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn=30&rn=30&gsm=1e&1560505489300=".format(category=quote(self.category))
        yield scrapy.Request(url=url,  callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp = json.loads(response.text)
        data = resp.get("data", [])

        img_urls = []
        for img in data:
            hover_url = img.get("middleURL")
            if hover_url:
                img_urls.append(hover_url)
                print(hover_url)

        item = ImgsItem()
        item["category"] = self.category
        item["image_urls"] = img_urls
        yield item

        # total_num = resp.get("displayNum")
        # current_num = re.findall('&pn=(.*?)&rn=30', response.url)[0]
        # if int(current_num) < int(total_num):
        #     url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={category}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={category}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn={page}&rn=30&gsm=1e&1560505489300=".format(
        #         category=quote(self.category), page=int(current_num)+30)
        #     yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

