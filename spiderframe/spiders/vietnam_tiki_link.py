# -*- coding: utf-8 -*-
import scrapy

from spiderframe.items import SpiderframeItem


class VietnamTikiLinkSpider(scrapy.Spider):
    name = 'vietnam_tiki_link'
    allowed_domains = ['tiki.vn']

    def __init__(self, category="Sách", *args, **kwargs):
        super(VietnamTikiLinkSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        # url = "https://tiki.vn/search?q={}".format(self.category)
        url = "https://tiki.vn/sach-truyen-tieng-viet/c316?order=top_seller&src=c.316.hamburger_menu_fly_out_banner"
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"page": 1})

    def parse(self, response):
        urls = response.xpath('//div[@class="product-box-list"]/div/a/@href').extract()
        for url in urls:
            item = SpiderframeItem()
            item['url'] = url
            item['ori_url'] = response.url
            yield item

        if urls:
            next_page = response.meta["page"] + 1
            page_url = 'https://tiki.vn/sach-truyen-tieng-viet/c316?order=top_seller&src=c.316.hamburger_menu_fly_out_banner&page={}'.format(
                next_page)
            yield scrapy.Request(url=page_url, callback=self.parse, dont_filter=True, meta={"page": next_page})
