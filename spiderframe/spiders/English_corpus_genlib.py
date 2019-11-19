# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class EnglishCorpusGenlibSpider(scrapy.Spider):
    name = 'English_corpus_genlib'
    allowed_domains = ['gen.lib.rus.ec']
    start_urls = ['http://gen.lib.rus.ec/']

    def start_requests(self):
        md5 = "798c486760812b47f6cd9416749da16c"

        with open(r"C:\Users\Administrator\Desktop\md5.txt", 'r', encoding='utf8')as f:
            for line in f:
                md5 = line.strip()
                url = "http://93.174.95.29/fiction/{md5}".format(**locals())
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        download_link = response.xpath('//*[@id="info"]/h2/a/@href').extract()
        download_url = "http://93.174.95.29/" + download_link[0]
        yield scrapy.Request(url=download_url, callback=self.parse_txt, dont_filter=True)

    def parse_txt(self, response):
        item = SpiderframeItem()
        item['url'] = response.url
        item['content'] = response.text
        yield item
