# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider

class NetherlandsAdContentSpider(RedisSpider):
    name = 'Netherlands_ad_content'
    allowed_domains = ['www.ad.nl']
    start_urls = 'https://www.ad.nl/show/duizenden-stemmen-voor-henk-blok-als-passion-verteller~ababad1f/'
    headers = {
        "Host": "www.ad.nl",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "text/html",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
        "Cookie": "pwv=2; pws=functional|analytics|content_recommendation|targeted_advertising|social_media; pwv=2; pws=functional|analytics|content_recommendation|targeted_advertising|social_media; _sp_id.b303=89ed612a-17d7-46e8-b0e8-c181515ef61f.1574303856.2.1574314909.1574303962.0d98937e-cf5e-43c4-942b-36a206db8403; _sotmpid=0:k383viln:qsHvFVdKmUe5LkiJr4u5cWj_49OuhBlD; gig_bootstrap_3_P5Nmq7DTo9xh8yVx5Vm74AVQEL4g1C_-STsGxC2efKVKj2r-GzbIyzUltSXtTo5v=accounts; _ga=GA1.2.1714854885.1574303879; _gid=GA1.2.495940355.1574303879; cX_S=k383vrzmbjuczeyo; cX_P=k383vrzonj79ic37; cstp=1; _hjid=8e29c318-48e2-444f-99b8-a878e2107f20; __gads=ID=3301de286ff274d2:T=1574303885:S=ALNI_MYO8cOJnJk5lGJQd6KnVTgxnDtLRA; _polar_tu=*_%22mgtn%22_@2Q_u_@_0c6df671-047e-42e7-acb6-33e43630e31a_Q_n_@3Q_s_@1Q_sc_@*_v_@1Q_a_@4+Q_ss_@_%22q1asnk_Q_sl_@_%22q1asnl_Q_sd_@*+Q_v_@_1%5Bd22464a_Q_vc_@*_e_@2+Q_vs_@_%22q1asnk_Q_vl_@_%22q1asnk_Q_vd_@*+Q_vu_@_2dd7a0aac6d0d48e466227df75615725_Q_vf_@_%22k383v68h_+; lastConsentChange=1574314910759; 104fc09b-ebf8-46a9-83a3-5c139fc7adaffaktorChecksum=2007867044; cto_lwid=94a36bcf-0b23-4a57-a797-3bebe00852d5; _gcl_au=1.1.480693782.1574303962; cto_bundle=FdALh18zU05pMk5UV2FwTGV5SyUyQnR4c2RiRTNoQjhoT2xYdnVnM2JDT3FDSEpDR1hyczhpTFRlNFpBcGo4RjFKWHBLRjNVa0Q5cW1rdndMcFR3Z2RQTVVLd1olMkZTMkxKSTZvZzhCalFXZE1VWnNOUnZuRSUyRmVhYVNleDVkM0dGSElINlhkajdhZUlnOTVlZ0MzWUI1eGxSOVNudlElM0QlM0Q; _sp_ses.b303=*; _sotmsid=0:k38ag6tt:UMjr65KjoPbAdMibUDL5NeA1JH9TRBHg; kntRedirect=true"
    }

    redis_key = 'Netherlands_ad_link'

    custom_settings = {
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, dont_filter=True, headers=self.headers)

    def parse(self, response):
        title = response.xpath('//h1/text()').extract()
        content = response.xpath('//p/text()').extract()
        content = ''.join(content)
        content = content.replace(" ","")
        item = SpiderframeItem()
        item['url'] = response.url
        item['category'] = response.url.split('/')[3]
        item['title'] = ''.join(title)
        item['content'] = content
        # print(item)
        yield item

