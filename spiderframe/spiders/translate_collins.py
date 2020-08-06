# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon


class TranslateCollinsSpider(scrapy.Spider):
    name = 'translate_collins'
    allowed_domains = ['www.collinsdictionary.com']
    start_urls = ['https://www.collinsdictionary.com/']

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(200000):
            item = ssdb_con.lpop("collins_word_urls")
            keyword = item.decode("utf8")
            url = "https://www.collinsdictionary.com/dictionary/english/{}".format(keyword)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        keyword = response.meta.get("keyword")
        show_word_l = response.xpath('//div/h2/span[@class="orth"]/text()').extract()
        if show_word_l:
            show_word = show_word_l[0]
        else:
            show_word = ""
        ph_en_l = response.xpath('//div[contains(@class, "Collins_Eng_Dict")]/div[1]//div[@class="mini_h2"]')
        if ph_en_l:
            ph_en = "".join(ph_en_l[0].xpath('.//span[@class="pron type-"]//text()').extract()).replace("\n", "")
        else:
            ph_en = ""

        ph_am_l = response.xpath('//div[contains(@class, "Large_US_Webster")]/div[1]//div[@class="mini_h2"]')
        if ph_am_l:
            ph_am = "".join(ph_am_l[0].xpath('.//span[@class="pron type-ipa"]//text()').extract()).replace("\n", "")
        else:
            ph_am = ""

        un_phonetic_l = response.xpath(
            '//div[@class="dictionary Cob_Adv_Brit dictentry"]//span[@class="pron type-"]//text()').extract()
        if un_phonetic_l:
            un_phonetic = "".join(un_phonetic_l).strip()
        else:
            un_phonetic = ""
        item = SpiderframeItem()
        item['title'] = keyword  # title  字段 存单词
        item['category'] = show_word  # category 存显示的单词
        item['content'] = ph_en  # content 字段存 英式英语
        item['item_name'] = ph_am  # item_name 字段  美式英语
        item['item_id'] = un_phonetic  # item_id 字段  不确定是英式还是美式的情况
        yield item
