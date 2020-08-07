# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon


class TranslateLdoceonlineSpider(scrapy.Spider):
    name = 'translate_ldoceonline'
    allowed_domains = ['www.ldoceonline.com']
    start_urls = ['http://www.ldoceonline.com/']

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(200000):
            item = ssdb_con.lpop("ldoceonline_word_urls")
            keyword = item.decode("utf8")
            url = "https://www.ldoceonline.com/dictionary/{}".format(keyword)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        keyword = response.meta.get("keyword")
        show_word_l = response.xpath('//h1[@class="pagetitle"]/text()').extract()
        if show_word_l:
            show_word = show_word_l[0]
        else:
            show_word = ""
        un_phonetic_l = response.xpath('//div[@class="dictionary"]//span[@class="PRON"]/text()').extract()
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
