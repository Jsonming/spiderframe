# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import SpiderframeItem


class TranslateCambridageSpider(scrapy.Spider):
    name = 'translate_cambridage'
    allowed_domains = ['dictionary.cambridge.org/']
    start_urls = ['https://dictionary.cambridge.org/dictionary/english/good']

    custom_setting = {
        "DOWNLOAD_DELAY": 2
    }

    def parse(self, response):
        word = response.url.split("/")[-1].split("=")[-1]
        show_word, uk_phonetic, us_phonetic = '', '', ''
        di_title = response.xpath('//div[@class="di-title"]//span[@class="hw dhw"]')
        if di_title:
            show_word = ''.join(di_title[0].xpath("./text()").extract())

        uk_span = response.xpath(
            '//div[@class="pos-header dpos-h"]//span[@class="uk dpron-i "]/span[@class="pron dpron"]')
        if uk_span:
            uk_phonetic = ''.join(uk_span[0].xpath('.//text()').extract())
            if uk_phonetic:
                uk_phonetic = "[" + uk_phonetic.strip('/') + "]"

        us_span = response.xpath(
            '//div[@class="pos-header dpos-h"]//span[@class="us dpron-i "]/span[@class="pron dpron"]')
        if us_span:
            us_phonetic = ''.join(uk_span[0].xpath('.//text()').extract())
            if us_phonetic:
                us_phonetic = "[" + us_phonetic.strip('/') + "]"

        item = SpiderframeItem()
        item['title'] = word  # title  字段 存单词
        item['category'] = show_word  # category 存显示的单词
        item['content'] = uk_phonetic  # content 字段存 英式英语
        item['item_name'] = us_phonetic  # category 字段  美式英语
        yield item
