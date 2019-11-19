# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateCnkiSpider(scrapy.Spider):
    name = 'translate_cnki'
    allowed_domains = ['http://dict.cnki.net/']

    def start_requests(self):
        # with open(r'E:\code\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
        #     for key_word in f:
        #         keyword = key_word.strip()
        keyword="god"
        url = "http://dict.cnki.net/dict_result.aspx?searchword={keyword}".format(
            keyword=keyword)
        yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)


    def parse(self,response):
        keyword=response.meta.get("keyword")
        cses=response.xpath('//font[@class="text6"]//text()').extract()
        for cs in cses:
            cs=re.findall(r"^[0-9]*$",cs)
            if cs:
                for c in cs:
                    for page in range(1, 5):
                        url = "http://dict.cnki.net/dict_more_sen.aspx?searchword={keyword}&unvsm=&t=&s=0&c={c}&z=&page={page}".format(
                            keyword=keyword, c=c,page=page)
                        yield scrapy.Request(url=url, callback=self.parse_content, meta={'keyword': keyword}, dont_filter=True)

    def parse_content(self, response):
        lis = response.xpath('//span//tr/td/table//tr[3]/td/table//tr')
        for li in lis:
            lis_text = li.xpath('.//td[not(@class)]//text()').extract()
            sentens="".join(lis_text)
            if "未完全匹配句对" not in sentens and sentens!="":
                sentens=sentens.strip()
                md = md5(sentens)
                item = SpiderframeItem()
                item['content'] = sentens
                item['title'] = response.meta.get("keyword")
                item['category'] = 'cnki'
                item['item_id'] = md
                yield item

