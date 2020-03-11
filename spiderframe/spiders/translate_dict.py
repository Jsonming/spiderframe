# -*- coding: utf-8 -*-
import re
import scrapy
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateDictSpider(scrapy.Spider):
    name = 'translate_dict'
    allowed_domains = ['dict.cn']

    redis_key = 'dict_word_urls'
    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    # def start_requests(self):
    #     with open(r'D:\Workspace\workspace\work\English_word\lower_word.txt', 'r', encoding='utf8')as f:
    #         for key_word in f.readlines()[:5]:
    #             keyword = key_word.strip()
    #             url = "https://dict.cn/search?q={keyword}".format(keyword=keyword)
    #             yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        # sentens1 = response.xpath('//div[@class="layout sort"]//li//text()').extract()
        # sentens2 = response.xpath('//div[@class="layout patt"]//li//text()').extract()
        # sentens3 = response.xpath('//div[@class="layout auth"]//li//text()').extract()
        # sentenses = sentens1 + sentens2 + sentens3
        # for sentens in sentenses:
        #     if (sentens >= u'\u0041' and sentens <= u'\u005a') or (sentens >= u'\u0061' and sentens <= u'\u007a'):
        #         md = md5(sentens)
        #         item = SpiderframeItem()
        #         item['content'] = sentens
        #         item['title'] = response.meta.get("keyword")
        #         item['category'] = 'dict'
        #         item['item_id'] = md
        #         yield item

        # 抓取读音
        word = response.url.split("=")[-1]
        word_tag = response.xpath('//div[@class="word-cont"]/h1/text()').extract()  # 显示单词
        if word_tag:
            phonetic = response.xpath('//div[@class="phonetic"]/span')
            en_phonetic, am_phonetic = '', ''
            if phonetic:
                for item in phonetic:
                    pronounce_lang = item.xpath("./text()").extract()  # 根据标签区分英式和美式
                    if pronounce_lang:
                        pronounce_text = ''.join(pronounce_lang).strip()
                        pronounce_text = pronounce_text.replace(" '", '').replace("’", '')
                        if pronounce_text == "英":
                            en_phonetic = ''.join(item.xpath('./bdo[@lang="EN-US"]/text()').extract())
                        elif pronounce_text == "美":
                            am_phonetic = ''.join(item.xpath('./bdo[@lang="EN-US"]/text()').extract())

            item = SpiderframeItem()
            item['title'] = word  # title  字段 存单词
            item['category'] = word_tag[0]  # category 存显示的单词
            item['content'] = en_phonetic  # content 字段存 英式英语
            item['item_name'] = am_phonetic  # category 字段  美式英语
            yield item
