# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from spiderframe.items import SpiderframeItem


class SwitzerlandTagesanzeigerLinkSpider(scrapy.Spider):
    name = 'Switzerland_tagesanzeiger_link'
    allowed_domains = ['www.tagesanzeiger.ch']
    start_urls=["https://www.tagesanzeiger.ch/"]
    headers = {
        "Host": "www.tagesanzeiger.ch",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
        "Cookie": "creid=1650866339328277179; minidmp2_session_id=d619f9464ac4d7b4fb3d9ab2bbbb43fd; POPUPCHECK=1574477670758; minidmp2_uuid=37738ac116e91084ae7; minidmp2_uuid_ts=1574391270121; _gcl_au=1.1.551634472.1574391288; _ga=GA1.2.2028895420.1574391288; _gid=GA1.2.780213381.1574391288; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.tagesanzeiger.ch/%22%2C%22sref%22:%22%22%2C%22sts%22:1574391288601%2C%22slts%22:0}; dakt_2_uuid=68f0094116e91089b66; dakt_2_uuid_ts=1574391290741; dakt_2_session_id=FpLtsmLSDTXI9Kt; dakt_2_plugins_id=9843a683c56cfbd519e1448d9daa01bb0d743fb0; dakt_2_webglvendor_id=1861c3f89839eef1a0409c68c420814843ba2a7b; dakt_2_canvas_id=6866d0b89d2cf8aa37480c62e470736e01232ca0; dakt_2_font_id=1c6fc7dd241ef79897c7308c11126013496f79c2; dakt_2_webgl_id=d36094438e89ee7d9639e8bf86fcabfc80af24ee; _dc_gtm_UA-58327930-1=1; _gat_UA-58327930-1=1; __utma=150503987.2028895420.1574391288.1574391303.1574391303.1; __utmb=150503987.2.10.1574391303; __utmc=150503987; __utmz=150503987.1574391303.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_first=1; __utmt_second=1; _parsely_visitor={%22id%22:%22pid=9e208157a24cc42a5eae8f85c588c40c%22%2C%22session_count%22:1%2C%22last_session_ts%22:1574391288601}; __gads=ID=2ef9bc5d171ef058:T=1574391306:S=ALNI_MYodRplZuToCiGMbpRogS4bMaO_wg"
    }

    def parse(self, response):
        patterns = response.xpath('//div[@id="mainNav"]//ul//li/a/@href').extract()
        for link in patterns:
            if "http" in link:
                yield scrapy.Request(url=link, callback=self.parse_url, dont_filter=True,headers=self.headers)

    def parse_url(self, response):
        links = response.xpath('//h3/a/@href').extract()
        for link in links:
            link = urllib.parse.quote(link)
            link = "https://www.tagesanzeiger.ch"+link
            item = SpiderframeItem()
            item['url'] = link
            # print(item)
            yield item




