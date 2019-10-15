# -*- coding: utf-8 -*-
import scrapy
import demjson
import re
from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_ellotte'
    start_urls = ["https://display.ellotte.com/display-fo/shop"]


    def parse(self, response):
        img_urls = response.xpath('//div[@class="type"]/ul/li/a/@href').extract()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Referer": "https://display.ellotte.com/display-fo/categoryShop?dshopNo=10148",

            # "Cookie": "MALL_TYPE=ellotte; JSESSIONID=f0cb9bae-b8d0-40ad-894b-5416c482e9a1; EL_RECENT_SHOPPING_INFOMATION_NEW=2%25%3A%25Women+%3E+%ED%8B%B0%EC%85%94%EC%B8%A0%25%3A%2510072%25%3A%25categoryShop%25%7C%7C%252%25%3A%25Foods+%3E+%EA%B1%B4%EA%B0%95%2F%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%8B%9D%ED%92%88%25%3A%2510149%25%3A%25categoryShop%25%7C%7C%251%25%3A%251201814729%25%3A%25%5B%EC%82%B0%ED%83%80%EB%A7%88%EB%A6%AC%EC%95%84%EB%85%B8%EB%B2%A8%EB%9D%BC%5D%EC%9D%B4%EB%93%9C%EB%9E%84%EB%A6%AC%EC%95%84+%EC%88%98%EB%B6%84%ED%81%AC%EB%A6%BC+%EC%9D%B4%EB%93%9C%EB%9D%BC%EC%86%94+%EB%B0%94%EB%94%94%ED%81%AC%EB%A6%BC+2%EC%A2%85+%EC%A4%91+%ED%83%9D1%25%3A%25%EC%96%B4%EB%8F%84%EC%96%B4%EA%B9%8C%EC%82%AC%25%3A%2597000%25%3A%2597000%25%3A%251201814729_1.jpg%25%7C%7C%251%25%3A%251201159230%25%3A%25%ED%95%98%EC%9D%B4%EC%95%8C%EB%A3%A8%EB%A1%A0+%ED%95%84%EB%9F%AC+3%EC%A2%85+%EC%84%B8%ED%8A%B8%28%EC%95%84%EC%9D%B4%ED%81%AC%EB%A6%BC%2C%EB%8D%B0%EC%9D%B4%ED%81%AC%EB%A6%BC%2C%EB%82%98%EC%9D%B4%ED%8A%B8%ED%81%AC%EB%A6%BC%29%25%3A%25%EC%9C%A0%EC%84%B8%EB%A6%B0%28%ED%95%B4%EC%99%B8%EC%A7%81%EA%B5%AC%29%25%3A%2587100%25%3A%2587100%25%3A%251201159230_1.jpg%25%7C%7C%252%25%3A%25%ED%95%B4%EC%99%B8%EC%A7%81%EA%B5%AC+%3E+%EC%83%9D%ED%99%9C%EC%9A%A9%ED%92%88%25%3A%2514466%25%3A%25categoryShop%25%7C%7C%252%25%3A%25BAG+%26+ACC+%3E+%EB%AA%85%ED%92%88+%EC%9D%98%EB%A5%98%2F%EC%8A%88%EC%A6%88%25%3A%2515009%25%3A%25categoryShop%25%7C%7C%25; lotte40UniqUserKey=1570675810727_51479; _ga=GA1.2.585961109.1570675815; _gid=GA1.2.1907396622.1570675815; alido_pcid=jBefSxftpNy0Kexc6sKMo; alido_agree=Y; cto_lwid=fe491216-2ec6-4ebc-a940-3025b2f58b59; grb_id_permission@b0b0b3c0=success; grb_ip_permission@b0b0b3c0=success; cto_bundle=gSAbt18zU05pMk5UV2FwTGV5SyUyQnR4c2RiRTFEMkJTYkNieVB5c2laYm5TN3ljWmt0SmpNUkpQa3dUTUVzaFdtVWMxJTJGcjJ1amRMblhpUGRkNUdRTk03bnlNS0xRbDFhVWdLa2NqamZ0bkxpZyUyRkZIU1V5UXlWSTdrNGhEcER6VVBUTndQdQ; grb_ck@b0b0b3c0=0b30299e-7484-62df-ed6f-b148a1f37919; grb_pv_st_tm@b0b0b3c0=%7B%22id%22%3A%22nullzzqqzz1zzqqzz2%22%2C%22time%22%3A23%7D; grb_ck_time@b0b0b3c0=1570676469865; grb_wg_op_st@b0b0b3c0=open; vs.bid=9KZAzH5OkT94hgFdGYkWEMU.k1k42me0; _gat=1; _gat_UA-116499776-2=1; _dc_gtm_UA-116499776-2=1; criteo_write_test=ChUIBBINbXlHb29nbGVSdGJJZBgBIAE"
        }
        for img_url in img_urls:
            pattern=re.findall(r"https://display.ellotte.com/display-fo/categoryShop\?(.*)",img_url)
            yield scrapy.Request(url="https://common.ellotte.com/common-fo/common/api/search/soaring", headers=headers,callback=self.parse_url, dont_filter=True,meta={'pattern': pattern})

    def parse_url(self, response):
        pattern = response.meta['pattern']
        resp = demjson.decode(response.text)
        data = resp.get("data")
        suddenKeywordList=data.get("suddenKeywordList")
        for goodsList in suddenKeywordList:
            goodsList=goodsList.get("goodsList")
            for goodsNo in goodsList:
                goodsNo = goodsNo.get("goodsNo")
                url="http://goods.ellotte.com/goods-fo/goodsDetail/{goodsNo}?{pattern}".format(goodsNo=goodsNo,pattern=pattern[0])
                yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True,meta={'pattern': pattern})

    def parse_content(self, response):
        pattern = response.meta['pattern']
        img_urls = response.xpath('//a[@id="detailsGallery_opener"]/img/@data-zoom-image').extract()
        item = ImgsItem()
        item["image_urls"] = img_urls
        item["category"] = pattern[0]
        yield item
