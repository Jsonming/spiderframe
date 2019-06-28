# -*- coding: utf-8 -*-
import scrapy
import json
from urllib import parse
from ..items import SpiderframeItem


class ChinaNewsPeopleSpider(scrapy.Spider):
    name = 'china_news_people_link'
    allowed_domains = ['www.people.com.cn']
    start_urls = [
        # 'http://news.people.com.cn/',
        # 'http://news.people.com.cn/210801/211150/index.js?_=1561705417484'

        # 'http://politics.people.com.cn/',
        # 'http://world.people.com.cn/',
        # 'http://finance.people.com.cn/',
        # 'http://tw.people.com.cn/',
        # 'http://military.people.com.cn/',
        # 'http://opinion.people.com.cn/',
        # 'http://leaders.people.com.cn/',
        # 'http://renshi.people.com.cn/',
        # 'http://theory.people.com.cn/',
        # 'http://legal.people.com.cn/',
        # 'http://society.people.com.cn/',
        # 'http://industry.people.com.cn/',
        # 'http://sports.people.com.cn/',
        # 'http://art.people.com.cn/',
        # 'http://house.people.com.cn/',
        # 'http://scitech.people.com.cn/',

        # 'http://kpzg.people.com.cn/',
        # 'http://culture.people.com.cn/',
        # 'http://auto.people.com.cn/',
        # 'http://health.people.com.cn/',

        # 'http://edu.people.com.cn/',
        # "http://edu.people.com.cn/GB/392532/index.html",
        # "http://edu.people.com.cn/GB/228146/index.html",

        # "http://edu.people.com.cn/GB/227065/index.html",
        # "http://edu.people.com.cn/GB/227057/index.html",
        # "http://edu.people.com.cn/GB/226718/index.html",
        # "http://edu.people.com.cn/GB/204387/204389/index.html",
        # "http://edu.people.com.cn/GB/208610/index.html",
        # "http://edu.people.com.cn/GB/gaokao/",
    ]

    def parse(self, response):
        # data = json.loads(response.text)
        # items = data.get("items")
        # for item in items:
        #     url = item.get("url")
        #     item = SpiderframeItem()
        #     item['url'] = url
        #     yield item

        ori_url_parm = parse.urlsplit(response.url)
        links = response.xpath('//div[@class="hdNews clearfix"]//a/@href').extract()

        links = response.xpath('//ul[@class="list_14b"]//a/@href').extract()
        links = response.xpath('//ul[@class=" list_16 mt10"]//a/@href').extract()
        links = response.xpath('//dl[@class="list_14"]//a/@href').extract()
        links = response.xpath('//ul[@class="list_14 mt15"]//a/@href').extract()

        urls = ["http://" + ori_url_parm.netloc + item for item in links]
        for url in urls:
            item = SpiderframeItem()
            item['url'] = url
            yield item

        next_page = response.xpath('//*[@id="p2Ab_1"]/div[13]/a[last()]/@href').extract_first()
        next_page = response.xpath('//div[@class="page"]/a[last()]/@href').extract_first()
        next_page = response.xpath('//div[@class="page_n clearfix"]/a[last()]/@href').extract_first()
        param = response.url.split('/')[-1]
        next_page_url = response.url.replace(param, '') + next_page
        yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
