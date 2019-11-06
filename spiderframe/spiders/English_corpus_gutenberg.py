# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import SpiderframeItem


class EnglishCorpusGutenbergSpider(scrapy.Spider):
    name = 'English_corpus_gutenberg'
    allowed_domains = ['www.gutenberg.org']
    # start_urls = ['http://www.gutenberg.org/ebooks/search/%3Fsort_order%3Ddownloads']

    def start_requests(self):
        for i in range(26, 1000, 25):
            url = "http://www.gutenberg.org/ebooks/search/?sort_order=downloads&start_index={}".format(i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        book_links = response.xpath('//li[@class="booklink"]//a/@href').extract()
        for book_link in book_links:
            book_url = "https://www.gutenberg.org" + book_link
            yield scrapy.Request(url=book_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        content_link = response.xpath('//a[contains(@type, "text/plain")]/@href').extract()
        if "ebook" in content_link[0]:
            content_id = content_link[0].split('.')[0]
            content_url_id = content_id.split("/")[-1]
            content_url = "http://www.gutenberg.org/cache/epub/{}/pg{}.txt".format(content_url_id, content_url_id)
        else:
            content_url = "https://www.gutenberg.org" + content_link[0]
        yield scrapy.Request(url=content_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        content = response.text
        item = SpiderframeItem()
        item['url'] = response.url
        item['content'] = content
        yield item
