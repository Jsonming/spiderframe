# -*- coding: utf-8 -*-
import scrapy


class ChinaNewsPeopleContentSpider(scrapy.Spider):
    name = 'china_news_people_content'
    allowed_domains = ['culture.people.com']
    start_urls = ['http://culture.people.com.cn/n1/2019/0619/c1013-31167605.html']

    def parse(self, response):
        content = response.xpath('//div[@class="box_con"]/p/text()').extract()
        print(content)
