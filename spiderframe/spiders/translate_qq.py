# -*- coding: utf-8 -*-
import json
import re

import scrapy

from spiderframe.script.qq_translate_js import Py4Js
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateQQSpider(scrapy.Spider):
    name = 'translate_qq'
    allowed_domains = ['fanyi.qq.com/']
    start_urls = ['https://fanyi.qq.com/']

    def start_requests(self):
        with open(r'D:\Workspace\spiderframe\spiderframe\files\commen_words.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                pj = Py4Js()
                tk = pj.get_tk(keyword)
                # url = "https://dictweb.translator.qq.com/?channel=pc&download=no&logo=no&ADTAG=PCWEB&id={id}".format(**locals())
                url = "https://dictweb.translator.qq.com/api/wordnet?id={id}".format(**locals())
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        resp = json.loads(response.text)
        for sentence in resp["data"]:
            for exp1 in sentence:
                for exp2 in exp1["data"]:
                    for exp in exp2:
                        if exp:
                            md = md5(exp)
                            item = SpiderframeItem()
                            item['content'] = exp
                            item['title'] = response.meta.get("keyword")
                            item['category'] = 'qq'
                            item['item_id'] = md
                            # yield item
                            print(item)