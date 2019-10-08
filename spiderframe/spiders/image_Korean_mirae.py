# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import quote
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_mirae'
    start_urls = ["https://textbookmall.mirae-n.com/"]

    def parse(self, response):
        urls = response.xpath('//div[@class="inner"]/ul/li/a/@href').extract()
        for url in urls:
            if "http://textbookmall.mirae-n.com/asp/sub/" in url:
                url_split = re.split("/", url)
                pattern = re.findall(r"Product_main.asp\?(.*)",url_split[-1])
                true_urls=[str(url)+r"#Page={i}&{pattern}&SCode3=&PageSize=24^P^list".format(i=i,pattern=pattern[0])for i in range(1,11)]
                for true_url in true_urls:
                    yield scrapy.Request(url=true_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//ul[@class="small-list"]/li/a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//dd//img/@src').extract()
        category = response.xpath('//option[@selected=""]//text()').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] = category
        yield item
