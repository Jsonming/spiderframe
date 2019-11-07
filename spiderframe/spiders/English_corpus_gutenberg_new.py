# -*- coding: utf-8 -*-
import scrapy
from ..items import SpiderframeItem


class EnglishCorpusGutenbergNewSpider(scrapy.Spider):
    name = 'English_corpus_gutenberg_new'
    allowed_domains = ['www.gutenberg.org/dirs']
    start_urls = [
        'http://www.gutenberg.org/dirs/0/',
        'http://www.gutenberg.org/dirs/1/',
        'http://www.gutenberg.org/dirs/2/',
        'http://www.gutenberg.org/dirs/3/',
        'http://www.gutenberg.org/dirs/4/',
        'http://www.gutenberg.org/dirs/5/',
        'http://www.gutenberg.org/dirs/6/',
        'http://www.gutenberg.org/dirs/7/',
        'http://www.gutenberg.org/dirs/8/',
        'http://www.gutenberg.org/dirs/9/',
    ]

    def parse(self, response):
        ori_url = response.url
        sub_dir = response.xpath("//tr//a/@href").extract()
        for sub_dir_index in sub_dir[1:]:
            new_url = ori_url + sub_dir_index
            yield scrapy.Request(url=new_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        content_ori_url = response.url
        content_url_mark = response.xpath("//tr//a/@href").extract()
        for content_url_index in content_url_mark:
            if "txt" in content_url_index:
                content_url = content_ori_url + content_url_index
                yield scrapy.Request(url=content_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        content = response.text
        item = SpiderframeItem()
        item['url'] = response.url
        item['content'] = content
        yield item
