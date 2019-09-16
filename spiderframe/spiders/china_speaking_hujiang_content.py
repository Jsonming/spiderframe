# -*- coding: utf-8 -*-
import scrapy

from ..items import SpiderframeItem


class ChinaSpeakingHujiangContentSpider(scrapy.Spider):
    name = 'china_speaking_hujiang_content'
    allowed_domains = ['http://www.hjenglish.com']
    start_urls = ['http://www.hjenglish.com/yanjiang/p1088489/']

    def parse(self, response):
        title = response.xpath('//div[@class="article-header"]//text()').extract_first()
        paragrah = response.xpath('//div[@class="article-content"]//p/text()').extract()

        content = []
        content.extend(title)
        content.extend(paragrah)
        content = ''.join(content).replace('\n', '').replace('\t', '').replace('\r', '')
        item = SpiderframeItem()
        item['url'] = response.url
        item['content'] = content
        print(item)
