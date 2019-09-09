# -*- coding: utf-8 -*-
import scrapy
import json
from spiderframe.items import ImgsItem



class IndiaHindiLinkSpider(scrapy.Spider):
    name = 'india_hindi_image'
    allowed_domains = ['hindi.webdunia.com']

    # start_urls = [
    #     'https://hindi.webdunia.com/indian-festivals?utm_source=Top_Nav_Article&utm_medium=Site_Internal/1/{}'.format(i)
    #     for i in range(2, 4)]

    def start_requests(self):
        for i in range(2, 100):
            url = "https://hindi.webdunia.com/core/home-page/more-category-news"
            form_data = {"page": str(i), "item_per_page": '', "category_id": '1060300000', "category_creation_id": '10603'}

            yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse, dont_filter=True)

    def parse(self, response):
        images = response.xpath(r'//div[@id="contentListingData"]/div//img/@src').extract()
        images = response.xpath(r'//img/@src').extract()
        image_url = ["https:" + url for url in images]

        item = ImgsItem()
        item["category"] = "hindi"
        item["image_urls"] = image_url
        yield item
