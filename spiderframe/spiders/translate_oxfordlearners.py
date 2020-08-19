# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon


class TranslateOxfordlearnersSpider(scrapy.Spider):
    name = 'translate_oxfordlearners'
    allowed_domains = ['www.oxfordlearnersdictionaries.com']
    start_urls = ['https://www.oxfordlearnersdictionaries.com/']

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(200000):
            item = ssdb_con.lpop("oxfordlearners_word_urls")
            keyword = item.decode("utf8")
            url = "https://www.oxfordlearnersdictionaries.com/search/english/direct/?q={keyword}".format(keyword=keyword)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})


    def parse(self, response):
        show_word_r = response.xpath('//div[@class="webtop"]/h1/text()').extract()
        if show_word_r:
            show_word = show_word_r[0]
        else:
            show_word = ''
        ph_en_r = response.xpath(
            '//div[@class="webtop"]/span[@class="phonetics"]/div[@class="phons_br"]/span/text()').extract()
        if ph_en_r:
            ph_en = ph_en_r[0]
        else:
            ph_en = ''
        ph_am_r = response.xpath(
            '//div[@class="webtop"]/span[@class="phonetics"]/div[@class="phons_n_am"]/span/text()').extract()
        if ph_am_r:
            ph_am = ph_am_r[0]
        else:
            ph_am = ''

        item = SpiderframeItem()
        item['title'] = response.meta.get("keyword")  # title  字段 存单词
        item['category'] = show_word  # category 存显示的单词
        item['content'] = ph_en  # content 字段存 英式英语
        item['item_name'] = ph_am  # category 字段  美式英语
        return item
