# -*- coding: utf-8 -*-
import scrapy
import re


class ImageGoogleSpider(scrapy.Spider):
    name = 'image_google'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.google.com/search?ei=BrcIXeikOYWJr7wPrYaIuAU&yv=3&q=%E7%8C%AB&tbm=isch&vet=10ahUKEwjov5bW4_LiAhWFxIsBHS0DAlcQuT0ITCgB.BrcIXeikOYWJr7wPrYaIuAU.i&ved=0ahUKEwjov5bW4_LiAhWFxIsBHS0DAlcQuT0ITCgB&ijn=1&start=100&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc']

    def parse(self, response):
        print(response.text)
