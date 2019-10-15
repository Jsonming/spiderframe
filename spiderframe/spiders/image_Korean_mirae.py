# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import quote
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_mirae'
    start_urls = ["https://textbookmall.mirae-n.com/"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        urls = response.xpath('//div[@class="inner"]/ul/li/a/@href').extract()
        for url in urls:
            if "http://textbookmall.mirae-n.com/asp/sub/" in url:
                url_split = re.split("/", url)
                pattern = re.findall(r"Product_main.asp\?(.*)",url_split[-1])
                true_urls=["http://textbookmall.mirae-n.com/ASP/Sub/Product_list_ajax.asp?Page={i}&{pattern}&SCode3=&PageSize=24&ListType=list&Sort=P".format(i=i,pattern=pattern[0])for i in range(1,11)]
                for true_url in true_urls:
                    yield scrapy.Request(url=true_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//ul/li/a/@href').extract()
        for img_url in img_urls:
            print(img_url)
            if "http://textbookmall.mirae-n.com/Asp/Sub/product_view.asp?" in img_url:
                yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//p//img/@src').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] = "textbookmall"
        yield item
