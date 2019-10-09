# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_yes24'
    # start_urls = ["http://cn.yes24.com"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = "http://www.yes24.com/"
       #  headers = {
       #      "User-Agent": "Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/69.0",
       #      "Cookie":"PCID=15705230219801830925000; cartCookieCnt=0; RecentViewGoods=; RecentViewInfo=NotCookie%3DY%26Interval%3D5; wcs_bt=s_1b6883469aa6:1570582801; __utma=12748607.1824039958.1570523097.1570523097.1570582802.2; __utmz=12748607.1570523097.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1824039958.1570523097; _gid=GA1.2.2003353712.1570523707; yes24_glbola_redirect=value=https%3A%2F%2Fcn.yes24.com%2F; HTTP_REFERER=; WiseLogParam=Null; __utmc=12748607; ASP.NET_SessionId=v4i2a345en2kgjr3oo25pkur; __utmb=12748607.1.10.1570582802; __utmt=1",
       #      # "Accept":"text / html, application / xhtml + xm…plication / xml;q = 0.9, * / *;q = 0.8",
       #      # "Accept - Encoding":"gzip, deflate",
       #      # "Accept - Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
       #      # "Cache - Control":"max - age = 0",
       #      "Connection":"keep-alive",
       #      "Host":"www.yes24.com"	,
       #      "Upgrade-Insecure-Requests":"1"
       # }
        # cookie={
        #         "__utma":"12748607.1824039958.1570523097.1570523097.1570523097.1",
        #         "__utmb":"12748607.5.10.1570523097",
        #         "__utmc":"12748607",
        #         "__utmz":"12748607.1570523097.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        #         "_gz":"GA1.2.1824039958.1570523097",
        #         "_gid": "GA1.2.2003353712.1570523707",
        #         "ASP.NET_SessionId":"v4i2a345en2kgjr3oo25pkur",
        #         "cartCookieCnt":"0",
        #         "HTTP_REFERER"
        #         "PCID":"15705230219801830925000",
        #         "RecentViewGoods"
        #         "RecentViewInfo":"NotCookie=Y&Interval=5",
        #          "wcs_bt":"s_1b6883469aa6:1570526170",
        #          "WiseLogParam":"Null",
        #          "yes24_glbola_redirect":"value=https://cn.yes24.com/"
        # }
        headers ={
         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
         "Cookie": "PCID=15705230219801830925000; cartCookieCnt=0; RecentViewGoods=; RecentViewInfo=NotCookie%3DY%26Interval%3D5; wcs_bt=s_1b6883469aa6:1570591442; __utma=12748607.1824039958.1570523097.1570585177.1570591444.4; __utmz=12748607.1570523097.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1824039958.1570523097; _gid=GA1.2.2003353712.1570523707; yes24_glbola_redirect=value=https%3A%2F%2Fcn.yes24.com%2F; HTTP_REFERER=; WiseLogParam=Null; __utmc=12748607; ASP.NET_SessionId=v4i2a345en2kgjr3oo25pkur; __utmb=12748607.1.10.1570591444; __utmt=1"
        }

        yield scrapy.Request(url=url, headers=headers,callback=self.parse, dont_filter=True)


    # def parse(self, response):
    #     # urls = response.xpath('//dd[@class="qCatePos01"]//a/@href').extract()"/html/body/div/div[1]/div[1]/ul/li[6]/a
    #     urls = response.xpath('/html/body/div/div[1]/div[1]/ul/li[6]/a/@href').extract()
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)

    def parse(self, response):
        img_urls = response.xpath('//dd[@class="qCatePos01"]//a/@href').extract()
        for img_url in img_urls:
            img_url = "http://www.yes24.com/" + img_url
            # yield scrapy.Request(url=img_url, callback=self.parse_img, dont_filter=True)
            print(img_url)

    # def parse_url(self, response):
    #     img_urls = response.xpath('//div[@class="cateSubListArea clearfix"]/dl/dt/a/@href').extract()
    #     for img_url in img_urls:
    #         img_url="http://www.yes24.com/"+img_url
    #         yield scrapy.Request(url=img_url, callback=self.parse_img, dont_filter=True)
    #
    # def parse_img(self, response):
    #     img_urls = response.xpath('//span[@class="imgBdr"]/a/@href').extract()
    #     for img_url in img_urls:
    #         img_url="http://www.yes24.com/"+img_url
    #         # yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)
    #         print(img_url)

    # def parse_content(self, response):
    #     img_urls = response.xpath('//dd//img/@src').extract()
    #     category = response.xpath('//option[@selected=""]//text()').extract()
    #     item = ImgsItem()
    #     item["image_urls"] = img_urls
    #     item["category"] = category
    #     yield item
