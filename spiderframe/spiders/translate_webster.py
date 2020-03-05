# -*- coding: utf-8 -*-
import re
import scrapy


class TranslateWebsterSpider(scrapy.Spider):
    name = 'translate_webster'
    allowed_domains = ['www.merriam-webster.com']
    # start_urls = ['https://www.merriam-webster.com/browse/thesaurus/{}'.format(chr(i)) for i in
    #               range(ord("b"), ord("z") + 1)]
    start_urls = ["https://www.merriam-webster.com/browse/thesaurus/a"]

    def parse(self, response):
        words = response.xpath('//div[@class="entries"]//a/text()').extract()
        with open(r'D:\Workspace\spiderframe\spiderframe\files\webster_word.txt', 'a', encoding='utf8')as f:
            for word in words:
                f.write(word + "\n")

        next_page = response.xpath('//ul[@class="pagination"]/li[@class="next"]/a/@href').extract()
        next_url = "https://www.merriam-webster.com" + next_page[0]
        yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)
