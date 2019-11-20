# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import SpiderframeItem


class EgyptMasrawyLinkSpider(scrapy.Spider):
    name = 'Egypt_masrawy_link'
    allowed_domains = ['www.masrawy.com/']
    start_urls = ["https://www.masrawy.com/"]

    def parse(self, response):
        patterns = response.xpath('//nav//ul//li//a/@href').extract()
        for pattern in patterns:
            patt = re.findall(r'ection\/(.*?)\/\.*?#Nav',pattern)
            if patt:
                for i in range(1,94):
                    link="https://www.masrawy.com/listing/SectionMore?categoryId={patt}&pageIndex={i}&hashTag=SectionMore".format(i=i,patt=patt[0])
                    yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        links = response.xpath('//a[@class="item"]/@href').extract()
        for link in links:
            link="https://www.masrawy.com"+link
            item = SpiderframeItem()
            item['url'] = link
            yield item


