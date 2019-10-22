# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_video-biglobe'
    start_urls = ["http://video-biglobe.crank-in.net/"]
    # start_urls = ["http://video-biglobe.crank-in.net/movie/foreign",
    #               "http://video-biglobe.crank-in.net/movie/japanese",
    #               "http://video-biglobe.crank-in.net/search?genre=3",
    #               "http://video-biglobe.crank-in.net/search?genre=237",
    #               "http://video-biglobe.crank-in.net/search?genre=6",
    #               "http://video-biglobe.crank-in.net/search?genre=218"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        img_urls = response.xpath('//div[@class="fmenu clearfix"]/ul/li/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//dd[@class="more"]/a/@href').extract()
        for img_url in img_urls:
            img_url = "https://video-biglobe.crank-in.net" + img_url
            yield scrapy.Request(url=img_url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        next_urls = response.xpath('//span[@class="next"]/a/@href').extract()
        for next_url in next_urls:
            yield scrapy.Request(next_url, callback=self.parse_list)
        img_urls = response.xpath('//div[@class="photo"]/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//div[@class="photo"]/img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] = "image_video-biglobe"
        yield item

"""一部分属性为‘photo_area left’的img没抓到"""