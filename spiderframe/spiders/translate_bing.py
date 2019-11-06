# -*- coding: utf-8 -*-
import scrapy
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem


class TranslateBingSpider(scrapy.Spider):
    name = 'translate_bing'
    allowed_domains = ['cn.bing.com/']

    def start_requests(self):
        with open(r'E:\code\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                for offset in range(10, 50, 10):
                    url = "https://cn.bing.com/dict/service?q={keyword}&offset={offset}&dtype=sen&&qs=n&form=Z9LH5&sp=-1&pq={keyword}".format(
                        keyword=keyword, offset=offset)
                    yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        lis = response.xpath('//div[@class="se_li"]')
        for li in lis:
            sen_en = li.xpath(".//div[@class='sen_en']//text()").extract()
            sentens = "".join(sen_en)
            md = md5(sentens)
            item = SpiderframeItem()
            item['content'] = sentens
            item['title'] = response.meta.get("keyword")
            item['category'] = 'bing'
            item['item_id'] = md
            yield item

