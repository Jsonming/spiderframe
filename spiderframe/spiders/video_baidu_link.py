# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class VideoBaiduLinkSpider(scrapy.Spider):
    name = 'video_baidu_link'
    allowed_domains = ['www.baidu.com']
    start_urls = [
        "https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&lid=d7ad906200041879&ie=utf-8&wd=%E5%8C%96%E5%A6%86%E8%A7%86%E9%A2%91&rsv_spt=7&rsv_bp=1&f=8&oq=%E5%8C%96%E5%A6%86%E8%A7%86%E9%A2%91&rsv_pq=d7ad906200041879&rsv_t=fec1HR70aHwlq6Xv6GSy7F0wBBvAgTGrZEREJxSn8MsHcJj4OZyQFlCENr0dJniLN%2B%2Bf&async=1&pn=10"
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="video_list video_short"]/a/@href').extract()
        for link in links:
            item = SpiderframeItem()
            item['url'] = link
            print(link)
            yield item

        current_page_url = response.url.split("=")
        current_page = current_page_url[-1]
        if int(current_page) <= 1000:
            next_page_url = "https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&lid=d7ad906200041879&ie=utf-8&wd=%E5%8C%96%E5%A6%86%E8%A7%86%E9%A2%91&rsv_spt=7&rsv_bp=1&f=8&oq=%E5%8C%96%E5%A6%86%E8%A7%86%E9%A2%91&rsv_pq=d7ad906200041879&rsv_t=fec1HR70aHwlq6Xv6GSy7F0wBBvAgTGrZEREJxSn8MsHcJj4OZyQFlCENr0dJniLN%2B%2Bf&async=1&pn={}".format(int(current_page) + 10)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
