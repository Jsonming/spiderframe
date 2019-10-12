# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class HebrewWallaContentSpider(scrapy.Spider):
    name = 'hebrew_walla_content'
    allowed_domains = ['news.walla.co.il/item/3197515']
    start_urls = ['http://news.walla.co.il/item/3197515']

    def parse(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract()
        # subtitle = response.xpath('//p[@class="subtitle"]/text()').extract()
        content = response.xpath('//section/p/text()').extract()

        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[2].split('.')[0]
        item['title'] = ''.join(title)
        item['content'] = ''.join(content)
        yield item
