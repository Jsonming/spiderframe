# -*- coding: utf-8 -*-
import re
import scrapy
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon


class TranslateWebsterSpider(scrapy.Spider):
    name = 'translate_webster'
    allowed_domains = ['www.merriam-webster.com']
    start_urls = ["https://www.merriam-webster.com/dictionary/accession"]

    def start_requests(self):
        keyword = "immortalise"
        url = "https://www.merriam-webster.com/dictionary/{}".format(keyword)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

        # ssdb_con = SSDBCon().connection()
        # for i in range(200000):
        #     item = ssdb_con.lpop("webster_word_urls")
        #     keyword = item.decode("utf8")
        #     url = "https://www.merriam-webster.com/dictionary/{}".format(keyword)
        #     yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        keyword = response.meta.get("keyword")
        show_word_l = response.xpath('//*[@id="left-content"]/div[1]/div[1]/h1/text()').extract()
        if show_word_l:
            show_word = show_word_l[0]
        else:
            show_word = ""
        un_phonetic_l = response.xpath('//*[@id="left-content"]/div[3]/div/span/span[@class="pr"]/text()').extract()
        if un_phonetic_l:
            un_phonetic = un_phonetic_l[0]
        else:
            un_phonetic = ""

        item = SpiderframeItem()
        item['title'] = keyword  # title  字段 存单词
        item['category'] = show_word  # category 存显示的单词
        item['content'] = ""  # content 字段存 英式英语
        item['item_name'] = ""  # item_name 字段  美式英语
        item['item_id'] = un_phonetic  # item_id 字段  不确定是英式还是美式的情况
        yield item