# -*- coding: utf-8 -*-
import scrapy
from ..items import SpiderframeItem


class ChinaSpeakingHujiangLinkSpider(scrapy.Spider):
    name = 'china_speaking_hujiang_link'
    allowed_domains = ['www.hjenglish.com']
    start_urls = ['http://www.hjenglish.com/yanjiang/tedyanjiang/']

    def parse(self, response):
        links = response.xpath('//div[@class="pane"]//a/@href').extract()
        urls = ['http://www.hjenglish.com' + link for link in links]
        for url in urls:
            item = SpiderframeItem()
            item['url'] = url
            item['ori_url'] = response.url
            yield item

        next_page = response.xpath('//a[@class="l-next"]/@href').extract_first()
        next_url = 'http://www.hjenglish.com' + next_page
        yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)
