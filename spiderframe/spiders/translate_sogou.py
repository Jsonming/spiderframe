# -*- coding: utf-8 -*-
import json

import scrapy


class TranslateSogouSpider(scrapy.Spider):
    name = 'translate_sogou'
    allowed_domains = ['fanyi.sogou.com']
    start_urls = ['https://fanyi.sogou.com/']

    def start_requests(self):
        url = 'https://fanyi.sogou.com/reventondc/translateV2'
        form_data = {
            'from': 'auto',
            'to': 'zh - CHS',
            'text': 'good',
            'client': 'pc',
            'fr': 'browser_pc',
            'pid': 'sogou - dict - vr',
            'dict': 'true',
            'word_group': 'true',
            'second_query': 'true',
            'uuid': '46129f4c-6863-4aca-bf6a-bacee3f76699',
            'needQc': '1',
            's': 'ee7c9fe819d1d201c12c3b0b07279819'

        }
        yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse)

    def parse(self, response):
        print(response.text)
