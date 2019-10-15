# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import quote
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_ssg'

    def __init__(self, category="간식", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Cookie": "PCID=15697280214464170027313; cto_lwid=e5b4e1f6-7b9f-49fd-9d4e-da992e153020; RC_COLOR=24; RC_RESOLUTION=1920*1080; _xm_webid_1_=-658689738; CHECKED=f649158eebc511e9a65548df3770aa8611937095302023881; FSID=pz6rxw3f1m2y72kcvnm2; CKWHERE=direct_ssg; SSGDOMAIN=www; CSTALK_POPUP_OPEN=null; ssglocale=zh_CN; googtrans=/ko/zh-CN; googtrans=/ko/zh-CN; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE; where=SE%3DN%26CHNL_ID%3D0000015208%26CK_WHERE%3Ddirect_ssg%26ET%3D1570758420336%26et%3D1570758420511; FSID1=pz6syckcvnm3f1m2y726; JSESSIONID=5DCC61FEEAAAE2E232C3BC1D386AEC32.ssgmall1201",
            "Host": "www.ssg.com"
        }
        for i in range(1, 435):
            url = "http://www.ssg.com/search.ssg?target=all&query={category}&page={i}".format(category=quote(self.category), i=i)
            yield scrapy.Request(url=url,headers=headers, callback=self.parse, dont_filter=True)


    def parse(self, response):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Cookie": "PCID=15697280214464170027313; cto_lwid=e5b4e1f6-7b9f-49fd-9d4e-da992e153020; RC_COLOR=24; RC_RESOLUTION=1920*1080; _xm_webid_1_=-658689738; CHECKED=f649158eebc511e9a65548df3770aa8611937095302023881; FSID=pz6rxw3f1m2y72kcvnm2; CKWHERE=direct_ssg; SSGDOMAIN=www; CSTALK_POPUP_OPEN=null; ssglocale=zh_CN; googtrans=/ko/zh-CN; googtrans=/ko/zh-CN; where=SE%3DN%26CHNL_ID%3D0000015208%26CK_WHERE%3Ddirect_ssg%26ET%3D1570760426388%26et%3D1570760426538; FSID1=pz6ulbkcvnm3f1m2y725; JSESSIONID=510F3CE953BF4F538EC35E8AD5A3B755.ssgmall3203",
            "Host": "www.ssg.com"
        }
        ctgIds = response.xpath('//div[@class="thmb"]/a[@class="clickable"]/@href').extract()
        for ctgId in ctgIds:
            url = "http://www.ssg.com"+ctgId
            yield scrapy.Request(url=url, callback=self.parse_content,headers=headers, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//img[@id="mainImg"]/@src').extract()
        img_url="http:"+img_urls[0]
        item = ImgsItem()
        item["image_urls"] = [img_url]
        item["category"] = self.category
        yield item
