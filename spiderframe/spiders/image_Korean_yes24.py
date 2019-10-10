# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_yes24'

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = "http://www.yes24.com/"
        headers ={
         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
         "Cookie": "PCID=15705230219801830925000; cartCookieCnt=0; RecentViewGoods=; RecentViewInfo=NotCookie%3DY%26Interval%3D5; wcs_bt=s_1b6883469aa6:1570591442; __utma=12748607.1824039958.1570523097.1570585177.1570591444.4; __utmz=12748607.1570523097.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1824039958.1570523097; _gid=GA1.2.2003353712.1570523707; yes24_glbola_redirect=value=https%3A%2F%2Fcn.yes24.com%2F; HTTP_REFERER=; WiseLogParam=Null; __utmc=12748607; ASP.NET_SessionId=v4i2a345en2kgjr3oo25pkur; __utmb=12748607.1.10.1570591444; __utmt=1"
        }

        yield scrapy.Request(url=url, headers=headers,callback=self.parse, dont_filter=True)

    def parse(self, response):
        img_urls = response.xpath('//dd[@class="qCatePos01"]//a/@href').extract()
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        img_urls = response.xpath('//div[@class="cateSubListArea clearfix"]/dl/dt/a/@href').extract()
        for img_url in img_urls:
            img_url="http://www.yes24.com/"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_img, dont_filter=True)

    def parse_img(self, response):
        category = response.xpath('//em[@class="cate_tit"]//text()').extract()
        next_urls = response.xpath('//a[@class="bgYUI next"]/a/@href').extract()
        for next_url in next_urls:
            next_url="http://www.yes24.com"+next_url
            yield scrapy.Request(next_url, callback=self.parse_img)
        img_urls = response.xpath('//span[@class="imgBdr"]/a/@href').extract()
        for img_url in img_urls:
            img_url="http://www.yes24.com/"+img_url
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True,meta={'category': category})


    def parse_content(self, response):
        category = response.meta['category']
        img_urls = response.xpath('//em[@class="imgBdr"]//img/@src').extract()
        # print(img_urls)
        item = ImgsItem()
        # if "http://image.yes" in img_urls:
        item["image_urls"] = img_urls
        category = category[0]
        if "/" in category:
            category = re.sub("/", "", category)
            item["category"] = category.replace(" ","")
        else:
            item["category"] = category.replace(" ","")
        yield item
