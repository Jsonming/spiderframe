# -*- coding: utf-8 -*-
import json

import scrapy

from spiderframe.items import SpiderframeItem


class EnglishSpeakingTedLinkSpider(scrapy.Spider):
    name = 'English_speaking_ted_content'
    allowed_domains = ['ted2srt.org']
    start_urls = [
        'https://ted2srt.org/api/talks?offset={}'.format(i) for i in range(1000, 2000, 20)
    ]

    def parse(self, response):
        data = json.loads(response.body)
        for item in data:
            art_id = item.get('id')
            if art_id:
                url = "https://ted2srt.org/api/talks/{}/transcripts/txt?lang=en".format(art_id)
                yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item = SpiderframeItem()
        item["url"] = response.url
        item["content"] = response.text
        yield item
