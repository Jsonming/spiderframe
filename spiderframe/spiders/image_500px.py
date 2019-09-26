# -*- coding: utf-8 -*-

import scrapy
from lxml import etree
from spiderframe.items import ImgsItem
import demjson
from urllib.parse import quote


class ImageSpider(scrapy.Spider):
    name = 'image_500px'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        categorys = {0 : '未分类',1 : '抽象',10 : '胶片',11 : '艺术',12 : '美食',13 : '纪实',14 : '自然',15 : '微距',16 : '人物',17 : '表演',18 : '运动',19 : '静物',2 : '动物',20 : '交通',21 : '旅行',22 : '水下',23 : '婚礼',3 : '黑白',36 : '建筑',4 : '名人',43 : '风光',45 : '街拍',46 : '航拍',47 : '夜景',5 : '城市',6 : '商业',7 : '音乐',8 : '生活',9 : '时尚'}
        for key,value in categorys.items():
            for i in range(1,3):
                url = "https://500px.me/discover/rating?resourceType=0,2&category={key}&orderBy=rating&photographerType=&startTime=&page={i}&size=20&type=json".format(key=key,i=i)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,meta={'category': value})

    def parse(self, response):
        category=response.meta['category']
        page = response.text
        json_contents = demjson.decode(page)
        for json_content in json_contents["data"]:
            url = json_content["url"]
            image = url["baseUrl"]
            image_url=image+"!p4"
            item = ImgsItem()
            item["category"] = category
            item["image_urls"] = [image_url]
            yield item
