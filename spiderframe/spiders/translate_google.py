# -*- coding: utf-8 -*-
import json

import scrapy

from spiderframe.items import SpiderframeItem
from spiderframe.script.google_translate_js import Py4Js
from spiderframe.common.db import SSDBCon


class TranslateGoogleSpider(scrapy.Spider):
    name = 'translate_google'
    allowed_domains = ['translate.google.cn']
    start_urls = ['http://translate.google.cn/']
    custom_settings = {
        "DOWNLOAD_DELAY": 0.3
    }

    def start_requests(self):
        # 本地测试
        # with open(r'./files/data.txt', 'r', encoding='utf8')as f:
        #     for key_word in f.readlines()[100:120]:
        #         keyword = key_word.strip().split("\t")[0]
        #         keyword_len = len(keyword)
        #         pj = Py4Js()
        #         tk = pj.get_tk(keyword)
        #         # url = "https://translate.google.cn/translate_a/single?client=webapp&sl=en&tl=zh-CN&hl=zh-CN&dt=at&" \
        #         #       "dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ssel=3&tsel=3&kc=0&tk={tk}&q={keyword}".format(**locals())
        #         url = 'https://translate.google.cn/translate_tts?ie=UTF-8&q={keyword}&tl=en&total=1&idx=0' \
        #               '&textlen={keyword_len}&tk={tk}&client=webapp&prev=input'.format(**locals())
        #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

        ssdb_con = SSDBCon().connection()
        for i in range(200000):
            item = ssdb_con.lpop("google_word_urls")
            keyword = item.decode("utf8")
            keyword_len = len(keyword)
            pj = Py4Js()
            tk = pj.get_tk(keyword)
            #     url = "https://translate.google.cn/translate_a/single?client=webapp&sl=en&tl=zh-CN&hl=zh-CN&dt=at&" \
            #           "dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ssel=3&tsel=3&kc=0" \
            #           "&tk={tk}&q={keyword}".format(**locals())
            #     yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            url = 'https://translate.google.cn/translate_tts?ie=UTF-8&q={keyword}&tl=en&total=1&idx=0&textlen' \
                  '={keyword_len}&tk={tk}&client=webapp&prev=input'.format(**locals())
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})
        ssdb_con.close()

    def parse(self, response):
        # 抓读音
        with open(r'E:\video\google\{}_google.mp3'.format(response.meta.get("keyword")), 'wb')as f:
            f.write(response.body)

        # 抓取读音
        # word = response.url.split("=")[-1]
        # resp = json.loads(response.text)
        # word_tag = resp[0][0][1]
        # resp = resp[0][-1]
        # en_phonetic, am_phonetic = '', ''
        # if len(resp) == 4:
        #     pronun = resp[-1].split(",")
        #     if pronun:
        #         pronunciation = ["[" + item + "]" for item in pronun]
        #         if len(pronunciation) == 2:
        #             en_phonetic = pronunciation[0]
        #             am_phonetic = pronunciation[1]
        #         elif len(pronunciation) == 1:
        #             en_phonetic = pronunciation[0]
        #         else:
        #             print("*" * 200)
        #             print(pronunciation)
        #
        # item = SpiderframeItem()
        # item['title'] = word  # title  字段 存单词
        # item['category'] = word_tag  # category 存显示的单词  google没有跳转现实
        # item['content'] = en_phonetic  # content 字段存 英式英语
        # item['item_name'] = am_phonetic  # category 字段  美式英语
        # yield item
        # print(item)

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
