# -*- coding: utf-8 -*-
import scrapy
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateDictSpider(scrapy.Spider):
    name = 'translate_dict'
    allowed_domains = ['dict.cn']

    def start_requests(self):
        with open(r'E:\code\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                url = "https://dict.cn/search?q={keyword}".format(keyword=keyword)
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        sentens1 = response.xpath('//div[@class="layout sort"]//li//text()').extract()
        sentens2 = response.xpath('//div[@class="layout patt"]//li//text()').extract()
        sentens3 = response.xpath('//div[@class="layout auth"]//li//text()').extract()
        sentenses = sentens1 + sentens2 + sentens3
        for sentens in sentenses:
            if (sentens >= u'\u0041' and sentens <= u'\u005a') or (sentens >= u'\u0061' and sentens <= u'\u007a'):
                md = md5(sentens)
                item = SpiderframeItem()
                item['content'] = sentens
                item['title'] = response.meta.get("keyword")
                item['category'] = 'dict'
                item['item_id'] = md
                yield item
