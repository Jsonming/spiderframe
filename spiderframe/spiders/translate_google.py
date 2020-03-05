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
    custom_settings = {
        "DOWNLOAD_DELAY": 2
    }

    def start_requests(self):
        with open(r'D:\Workspace\spiderframe\spiderframe\files\commen_words.txt', 'r', encoding='utf8')as f:
            for key_word in f.readlines()[171000:]:
                keyword = key_word.strip()
                pj = Py4Js()
                tk = pj.get_tk(keyword)
                url = "https://translate.google.cn/translate_a/single?client=webapp&sl=en&tl=zh-CN&hl=zh-CN&dt=at&" \
                      "dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ssel=3&tsel=3&kc=0" \
                      "&tk={tk}&q={keyword}".format(**locals())
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        # 抓取读音
        resp = json.loads(response.text)[0][-1]
        if len(resp) == 4:
            pronunciation = resp[-1].split(",")
            pronunciation = ["["+item+"]" for item in pronunciation]
            with open(r'D:\Workspace\spiderframe\spiderframe\files\google_phonetic.txt', 'a', encoding='utf8')as f:
                f.write(response.meta.get("keyword") + "\t" + '\t'.join(pronunciation) + "\n")

        # 抓取例句
        # dr = re.compile(r'<[^>]+>', re.S)
        # resp = json.loads(response.text)[-1][0]
        # for sentence in resp:
        #     if sentence:
        #         sentence = sentence[0]
        #         if isinstance(sentence, str):
        #             sent = dr.sub('', sentence).strip()
        #             md = md5(sent)
        #             item = SpiderframeItem()
        #             item['content'] = sent
        #             item['title'] = response.meta.get("keyword")
        #             item['category'] = 'google'
        #             item['item_id'] = md
        #             yield item
