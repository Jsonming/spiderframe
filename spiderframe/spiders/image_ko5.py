# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import ImgsItem


class AbmormalCarAccidentSpider(scrapy.Spider):
    name = 'image_ko5'
    allowed_domains = ['www.ko5.com.cn/m/img']
    start_urls = ['http://www.ko5.com.cn/m/img/page/{}'.format(i) for i in range(52, 60)]

    def parse(self, response):
        links = response.xpath('//*[@id="post_container"]/li/div[2]/h2/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item, dont_filter=True)

        img_urls = response.xpath('//*[@id="post_container"]/li/div[1]/a/img/@src').extract()
        for img_url in img_urls:
            item = ImgLink()
            item['url'] = img_url
            yield item

    def parse_item(self, response):
        img_urls = response.xpath('//*[@id="post_content"]//img/@src').extract()
        for img_url in img_urls:
            item = ImgsItem()
            item['url'] = img_url
            yield item
