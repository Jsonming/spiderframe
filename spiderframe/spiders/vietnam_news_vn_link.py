# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem


class VietnamNewsVnLinkSpider(scrapy.Spider):
    name = 'vietnam_news_vn_link'
    allowed_domains = ['vnexpress.net/thoi-su']
    start_urls = [
        # "https://vnexpress.net/thoi-su",
        "https://vnexpress.net/kinh-doanh",
        # "https://vnexpress.net/giai-tri",
        # "https://vnexpress.net/phap-luat",
        # "https://vnexpress.net/giao-duc",
        # "https://vnexpress.net/suc-khoe",
        # "https://vnexpress.net/doi-song",
        # "https://vnexpress.net/du-lich",
        # "https://vnexpress.net/khoa-hoc",
        # "https://vnexpress.net/so-hoa",
        # "https://vnexpress.net/oto-xe-may",
        # "https://vnexpress.net/y-kien",
        # "https://vnexpress.net/tam-su",
        # "https://vnexpress.net/cuoi",
        # "https://vnexpress.net/goc-nhin"
        # "https://vnexpress.net/ajax/goc-nhin?category_id=1003450&page=7&exclude=3&rule=2"

    ]

    def parse(self, response):
        links = response.xpath('/html/body/section/section[1]/article/h4/a[1]/@href').extract()

        for url in links:
            item = SpiderframeItem()
            item['url'] = url
            print(url)
            yield item

        next_page = response.xpath('//*[@id="pagination"]/a[last()]/@href').extract_first()
        if not next_page:
            next_page = response.xpath('/html/body/section/section[1]/div[2]/a[last()]/@href').extract_first()
        if "vnexpress" not in next_page:
            next_page_url = "https://vnexpress.net" + next_page
        else:
            next_page_url = next_page
        yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
