# -*- coding: utf-8 -*-
import re
import json
import scrapy
from spiderframe.items import SpiderframeItem


class VideoBilibiliLinkSpider(scrapy.Spider):
    name = 'video_bilibili_link'
    allowed_domains = ['search.bilibili.com']

    def __init__(self, keyword="抢劫监控", *args, **kwargs):
        super(VideoBilibiliLinkSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword

    def start_requests(self):
        url = 'https://search.bilibili.com/all?keyword={}'.format(self.keyword)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'page': 1})

    def parse(self, response):

        links = response.xpath('//li[@class="video-item matrix"]/a/@href').extract()
        for link in links:
            if link.startswith('//'):
                link = "http:" + link
            item = SpiderframeItem()
            item['url'] = link
            yield item

        current_page = response.meta.get("page")
        if current_page <= 50 and links:
            next_page_num = int(current_page) + 1
            next_page_url = "https://search.bilibili.com/all?keyword={}&page={}".format(self.keyword, next_page_num)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True, meta={'page': next_page_num})
