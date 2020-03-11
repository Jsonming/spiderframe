# -*- coding: utf-8 -*-
import re

import scrapy

from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class TranslateBingSpider(RedisSpider):
    name = 'translate_bing'
    allowed_domains = ['cn.bing.com/']
    redis_key = 'bing_word_urls'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    # def start_requests(self):
        # 抓取例句
        # with open(r'E:\code\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
        #     for key_word in f:
        #         keyword = key_word.strip()
        #         for offset in range(10, 500, 10):
        #             url = "https://cn.bing.com/dict/service?q={keyword}&offset={offset}&dtype=sen&&qs=n&form=Z9LH5&sp=-1&pq={keyword}".format(
        #                 keyword=keyword, offset=offset)
        #             yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

        # 抓取音标
        # with open(r'D:\Workspace\workscript\work_script\demo.txt', 'r', encoding='utf8')as f:
        #     for key_word in f.readlines()[:]:
        #         keyword = key_word.strip().split()[0]
        #         url = "https://cn.bing.com/dict/search?q={}&qs=n&form=Z9LH5&sp=-1&pq=food&sc=8-4".format(keyword)
        #         yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        # 抓取例句
        # lis = response.xpath('//div[@class="se_li"]')
        # for li in lis:
        #     sen_en = li.xpath(".//div[@class='sen_en']//text()").extract()
        #     sentens = "".join(sen_en)
        #     md = md5(sentens)
        #     item = SpiderframeItem()
        #     item['content'] = sentens
        #     item['title'] = response.meta.get("keyword")
        #     item['category'] = 'bing'
        #     item['item_id'] = md
        #     yield item

        word = re.findall("q=(.*?)&qs=", response.url)[0]

        word_tag = response.xpath('//div[@class="hd_area"]//h1/strong/text()').extract()  # 显示单词
        if word_tag:
            # 抓取音标
            phonetic_us = response.xpath('//div[@class="hd_p1_1"]/div[@class="hd_prUS b_primtxt"]/text()').extract()
            if phonetic_us:
                phonetic_us_str = phonetic_us[0].replace("US\xa0", '')
            else:
                phonetic_us_str = ''

            phonetic_k = response.xpath('//div[@class="hd_p1_1"]/div[@class="hd_pr b_primtxt"]/text()').extract()
            if phonetic_k:
                phonetic_k_str = phonetic_k[0].replace("UK\xa0", '')
            else:
                phonetic_k_str = ""

            item = SpiderframeItem()
            item['title'] = word  # title  字段 存单词
            item['category'] = word_tag[0]  # category 存显示的单词
            item['content'] = phonetic_k_str  # content 字段存 英式英语
            item['item_name'] = phonetic_us_str  # category 字段  美式英语
            yield item
