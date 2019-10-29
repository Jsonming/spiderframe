# -*- coding: utf-8 -*-
import re
import scrapy
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateYoudaoSpider(scrapy.Spider):
    name = 'translate_youdao'
    allowed_domains = ['dict.youdao.com']

    def start_requests(self):
        with open(r'D:\datatang\spiderframe\spiderframe\files\new.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                start_url = 'http://dict.youdao.com/w/{}/'.format(keyword)
                yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        examples = response.xpath('//div[@class="examples"]/p[1]/text()').extract()
        dr = re.compile(r'<[^>]+>', re.S)

        if examples:
            for example in examples:
                collins_sentence = example.replace("...", '')
                collins_s = dr.sub('', collins_sentence).strip()
                md = md5(collins_s)
                item = SpiderframeItem()
                item['content'] = collins_s
                item['title'] = response.meta.get("keyword")
                item['category'] = 'youdao'
                item['item_id'] = md
                yield item

        examplesToggle = response.xpath('//div[@id="examplesToggle"]/div/ul/li/p[1]')
        if examplesToggle:
            for p_node in examplesToggle:
                p_node_str = ''.join(p_node.xpath('.//text()').extract()).strip()
                collins_sentence = p_node_str.replace("...", '')
                collins_s = dr.sub('', collins_sentence).strip()
                md = md5(collins_s)
                item = SpiderframeItem()
                item['content'] = collins_s
                item['title'] = response.meta.get("keyword")
                item['category'] = 'youdao'
                item['item_id'] = md
                yield item
