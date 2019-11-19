# -*- coding: utf-8 -*-
import scrapy
import re
import demjson
from spiderframe.items import SpiderframeItem


class SwedenAftonbladetLinkSpider(scrapy.Spider):
    name = 'sweden_aftonbladet_link'
    allowed_domains = ['www.aftonbladet.se/']
    start_urls = ["https://www.aftonbladet.se/"]

    def parse(self, response):
        # links = response.xpath("//a[(contains(@class, '_2PN35'))]/@href").extract()
        links = response.xpath('//a[@class="_2PN35"]/@href').extract()
        for link in links:
            if "https://" not in link and link:
                link="https://www.aftonbladet.se"+link
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        next_urls = response.xpath('//a[@class="_21Zor abBtn abThemeColor abThemeBorder"]//@href').extract()
        for next_url in next_urls:
            if "https://" not in next_url and "http://" not in next_url:
                pattern = re.split("/", next_url)
                if len(pattern)==3:
                    patt=pattern[1]+"="+pattern[2]
                    for i in range(0, 1000):
                        link = "https://www.aftonbladet.se/hyper-api/v1/pages/collections?pageId={i}&story={patt}".format(i=i, patt=patt)
                        yield scrapy.Request(url=link, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        resp = demjson.decode(response.text)
        data = resp.get("items", [])
        for v1 in data.values():
            for v2 in v1.values():
                if type(v2) is list and v2:
                    data1=v2[0]
                    if data1.get("target"):
                        expandedUri = data1["target"]["expandedUri"]
                        item = SpiderframeItem()
                        item['url'] = expandedUri
                        yield item


