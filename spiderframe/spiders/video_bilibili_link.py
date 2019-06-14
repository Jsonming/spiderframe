# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class VideoBilibiliLinkSpider(scrapy.Spider):
    name = 'video_bilibili_link'
    allowed_domains = ['search.bilibili.com']
    start_urls = ['https://search.bilibili.com/all?keyword=化妆视频&page=1']

    def parse(self, response):
        links = response.xpath('//*[@id="server-search-app"]/div[2]/div[2]/div/div[2]/ul/li/div/div[1]/a/@href').extract()
        for link in links:
            if link.startswith('//'):
                link = "http:" + link
            item = SpiderframeItem()
            item['url'] = link

            yield item

        current_page_url = response.url.split("=")
        current_page = current_page_url[-1]
        if int(current_page) <= 50:
            next_page_url = "https://search.bilibili.com/all?keyword=化妆视频&page={}".format(int(current_page) + 1)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
