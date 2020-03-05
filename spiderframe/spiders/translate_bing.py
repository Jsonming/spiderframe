# -*- coding: utf-8 -*-
import scrapy
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateBingSpider(scrapy.Spider):
    name = 'translate_bing'
    allowed_domains = ['cn.bing.com/']

    def start_requests(self):
        # 抓取例句
        # with open(r'E:\code\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
        #     for key_word in f:
        #         keyword = key_word.strip()
        #         for offset in range(10, 500, 10):
        #             url = "https://cn.bing.com/dict/service?q={keyword}&offset={offset}&dtype=sen&&qs=n&form=Z9LH5&sp=-1&pq={keyword}".format(
        #                 keyword=keyword, offset=offset)
        #             yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

        # 抓取音标
        with open(r'D:\Workspace\spiderframe\spiderframe\files\commen_words.txt', 'r', encoding='utf8')as f:
            for key_word in f.readlines()[200000:]:
                keyword = key_word.strip()
                url = "https://cn.bing.com/dict/search?q={}&qs=n&form=Z9LH5&sp=-1&pq=food&sc=8-4".format(keyword)
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        # 抓取例句
        # lis = response.xpath('//div[@class="se_li"]')
        # for li in lis:
        #     sen_en = li.xpath(".//div[@class='sen_en']//text()").extract()
        #     sentens = "".join(sen_en)
        #     md = md5(sentens)
        #     item = SpiderframeItem()
        #     item['content'] = sentens
        #     item['title'] = response.meta.get("keyword")
        #     item['category'] = 'bing'
        #     item['item_id'] = md
        #     yield item

        # 抓取音标
        phonetic_us = response.xpath('//div[@class="hd_p1_1"]/div[@class="hd_prUS b_primtxt"]/text()').extract()
        if phonetic_us:
            phonetic_us_str = phonetic_us[0].replace("US\xa0", '')
        else:
            phonetic_us_str = ''

        phonetic_k = response.xpath('//div[@class="hd_p1_1"]/div[@class="hd_pr b_primtxt"]/text()').extract()
        if phonetic_k:
            phonetic_k_str = phonetic_k[0].replace("UK\xa0", '')
        else:
            phonetic_k_str = ""
        pronunciation = (phonetic_k_str, phonetic_us_str)

        with open(r'D:\Workspace\spiderframe\spiderframe\files\bing_phonetic.txt', 'a', encoding='utf8')as f:
            f.write(response.meta.get("keyword") + "\t" + '\t'.join(pronunciation) + "\n")


