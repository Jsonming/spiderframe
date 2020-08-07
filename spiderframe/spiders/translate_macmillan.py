# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon


class TranslateMacmillanSpider(scrapy.Spider):
    name = 'translate_macmillan'
    allowed_domains = ['www.macmillandictionary.com']
    start_urls = ['http://www.macmillandictionary.com/']

    def start_requests(self):
        # keyword = "words"
        # url = "https://www.macmillandictionary.com/search/british/direct/?q={}".format(keyword)
        # yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

        ssdb_con = SSDBCon().connection()
        for i in range(200000):
            item = ssdb_con.lpop("macmillan_word_urls")
            keyword = item.decode("utf8")
            url = "https://www.macmillandictionary.com/search/british/direct/?q={}".format(keyword)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        keyword = response.meta.get("keyword")
        show_word_l = response.xpath('//h1/span[@class="BASE"]/text()').extract()
        if show_word_l:
            show_word = show_word_l[0]
        else:
            show_word = ""
        ph_en_l = response.xpath('//div[@id="entryContent"]//span[@class="PRON"]/text()').extract()
        if ph_en_l:
            ph_en = ph_en_l[0]
        else:
            ph_en = ""

        item = SpiderframeItem()
        item['title'] = keyword  # title  字段 存单词
        item['category'] = show_word  # category 存显示的单词
        item['content'] = ph_en  # content 字段存 英式英语
        item['item_name'] = ''  # item_name 字段  美式英语
        item['item_id'] = ''  # item_id 字段  不确定是英式还是美式的情况
        yield item
