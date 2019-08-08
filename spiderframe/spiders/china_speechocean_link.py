# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class ChinaSpeechoceanLinkSpider(scrapy.Spider):
    name = 'china_speechocean_link'
    allowed_domains = ['www.speechocean.com']
    start_urls = ['http://www.speechocean.com/datacenter/recognition/{}.html?prosearch=#datacenter_do'.format(i) for i in range(1, 60)]

    def parse(self, response):
        products = response.xpath('//div[@class="tit-list"]/div')
        for product in products:
            product_url = ''.join(product.xpath('.//a/@href').extract())
            product_id = ''.join(product.xpath('.//a//div[@class="t0"]/text()').extract())
            product_name = ''.join(product.xpath('.//a//div[@class="j0"]/text()').extract())
            product_time_long = ''.join(product.xpath('.//a//div[@class="num ft36"]/text()').extract())
            product_time_unit = ''.join(product.xpath('.//a//div[@class="n ft14"]/text()').extract())

            item = SpiderframeItem()
            item['item_id'] = product_id
            item['url'] = product_url
            item['item_name'] = product_name
            item['item_time_long'] = product_time_long
            item['item_time_unit'] = product_time_unit

            yield item

