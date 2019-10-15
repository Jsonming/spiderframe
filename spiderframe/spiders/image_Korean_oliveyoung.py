# -*- coding: utf-8 -*-
import scrapy
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_oliveyoung'
    start_urls = ["http://www.oliveyoung.co.kr/store/main/main.do"]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        isLoginCnts = response.xpath('//li/a/@data-ref-dispcatno').extract()
        for isLoginCnt in isLoginCnts:
            for i in range(1,3):
                url = "http://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo={isLoginCnt}&fltDispCatNo=&prdSort=01&pageIdx={i}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=8&aShowCnt=0&bShowCnt=0&cShowCnt=0".format(isLoginCnt=isLoginCnt,i=i)
                yield scrapy.Request(url=url, callback=self.parse_url, dont_filter=True)


    def parse_url(self, response):
        goodsnos = response.xpath('//a[@class="prd_thumb goodsList"]/@data-ref-goodsno').extract()
        dispcatnos = response.xpath('//a[@class="prd_thumb goodsList"]/@data-ref-dispcatno').extract()
        parameters=list(zip(goodsnos,dispcatnos))
        for parameter in parameters:
            img_url = "http://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo={i}&dispCatNo={j}".format(i=parameter[0],j=parameter[1])
            yield scrapy.Request(url=img_url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        img_urls = response.xpath('//div[@class="prd_img"]/img/@src').extract()
        img_url = re.sub("\?l=ko","", img_urls[0])
        category = response.xpath('(//a[@class="cate_y"])[1]/text()').extract()
        item = ImgsItem()
        item["image_urls"] = [img_url]
        if "/" in category:
            category = re.sub("/", "", category)
            item["category"] = category[0] + "image_oliveyoung"
        else:
            item["category"] = category[0] + "image_oliveyoung"
        yield item
