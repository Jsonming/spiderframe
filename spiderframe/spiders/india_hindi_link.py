# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import ImgsItem


class IndiaHindiLinkSpider(scrapy.Spider):
    name = 'india_hindi_link'
    allowed_domains = ['hindi.webdunia.com']
    start_urls = [
        'https://hindi.webdunia.com/indian-festivals?utm_source=Top_Nav_Article&utm_medium=Site_Internal/{}'.format(i)
        for i in range(1, 3)]

    def parse(self, response):
        images = response.xpath(r'//div[@id="contentListingData"]/div//img/@src').extract()
        image_url = ["https:" + url for url in images]
        print(image_url)

        item = ImgsItem()
        item["category"] = "hindi"
        item["image_urls"] = image_url
        yield item
