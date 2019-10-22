# -*- coding: utf-8 -*-
import json
import re

import scrapy

from spiderframe.script.google_translate_js import Py4Js
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateGoogleSpider(scrapy.Spider):
    name = 'translate_google'
    allowed_domains = ['translate.google.cn']
    start_urls = ['http://translate.google.cn/']

    def start_requests(self):
        with open(r'D:\datatang\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                pj = Py4Js()
                tk = pj.get_tk(keyword)
                url = "https://translate.google.cn/translate_a/single?client=webapp&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ssel=3&tsel=3&kc=0&tk={tk}&q={keyword}".format(
                    **locals())
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        dr = re.compile(r'<[^>]+>', re.S)
        resp = json.loads(response.text)[-1][0]
        for sentence in resp:
            if sentence:
                sentence = sentence[0]
                if isinstance(sentence, str):
                    sent = dr.sub('', sentence).strip()
                    md = md5(sent)
                    item = SpiderframeItem()
                    item['content'] = sent
                    item['title'] = response.meta.get("keyword")
                    item['category'] = 'google'
                    item['item_id'] = md
                    yield item
