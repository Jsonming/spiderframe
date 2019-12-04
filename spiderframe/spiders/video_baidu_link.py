# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import SpiderframeItem


class VideoBaiduLinkSpider(scrapy.Spider):
    name = 'video_baidu_link'
    allowed_domains = ['www.baidu.com']
    start_urls = [
        "https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&lid=afabdcd300025133&ie=utf-8&rsv_pq=afabdcd300025133&wd=%E7%BE%8E%E5%A6%86%E8%A7%86%E9%A2%91&rsv_spt=5&rsv_t=4c7cyMLufldoU9BC%2BTDPxbQK%2FVyYfLEyJXrb5ZyITQiWKVgfqEiSqtFPYlkQ0%2BxFPMgx&rsv_bp=1&f=8&async=1&pn=10"
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
            next_page_url ="https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&lid=afabdcd300025133&ie=utf-8&rsv_pq=afabdcd300025133&wd=%E7%BE%8E%E5%A6%86%E8%A7%86%E9%A2%91&rsv_spt=5&rsv_t=4c7cyMLufldoU9BC%2BTDPxbQK%2FVyYfLEyJXrb5ZyITQiWKVgfqEiSqtFPYlkQ0%2BxFPMgx&rsv_bp=1&f=8&async=1&pn={}".format(
                int(current_page) + 10)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)

"""美妆视频，化妆教程，妆前妆后，明星卸妆"""