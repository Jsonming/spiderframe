# -*- coding: utf-8 -*-
import scrapy
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateDictSpider(scrapy.Spider):
    name = 'translate_dict'
    allowed_domains = ['dict.cn']
    # custom_settings = {
    #     "DOWNLOAD_DELAY": 0.2
    # }

    def start_requests(self):
        with open(r'D:\Workspace\spiderframe\spiderframe\files\commen_words.txt', 'r', encoding='utf8')as f:
            for key_word in f.readlines()[200000:]:
                keyword = key_word.strip()
                url = "https://dict.cn/search?q={keyword}".format(keyword=keyword)
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        # sentens1 = response.xpath('//div[@class="layout sort"]//li//text()').extract()
        # sentens2 = response.xpath('//div[@class="layout patt"]//li//text()').extract()
        # sentens3 = response.xpath('//div[@class="layout auth"]//li//text()').extract()
        # sentenses = sentens1 + sentens2 + sentens3
        # for sentens in sentenses:
        #     if (sentens >= u'\u0041' and sentens <= u'\u005a') or (sentens >= u'\u0061' and sentens <= u'\u007a'):
        #         md = md5(sentens)
        #         item = SpiderframeItem()
        #         item['content'] = sentens
        #         item['title'] = response.meta.get("keyword")
        #         item['category'] = 'dict'
        #         item['item_id'] = md
        #         yield item

        # 抓取读音
        # print(response.text)
        phonetic = response.xpath('//bdo[@lang="EN-US"]/text()').extract()
        with open(r'D:\Workspace\spiderframe\spiderframe\files\dict_phonetic.txt', 'a', encoding='utf8')as f:
            f.write(response.meta.get("keyword") + "\t" + '\t'.join(phonetic) + "\n")
