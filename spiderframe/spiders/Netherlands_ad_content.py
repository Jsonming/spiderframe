# -*- coding: utf-8 -*-
from spiderframe.items import SpiderframeItem
from scrapy import FormRequest
from scrapy_redis.spiders import RedisSpider

class NetherlandsAdContentSpider(RedisSpider):
    name = 'Netherlands_ad_content'
    allowed_domains = ['www.ad.nl']
    start_urls = ['https://www.ad.nl/show/duizenden-stemmen-voor-henk-blok-als-passion-verteller~ababad1f/']
    headers = {
        "Host": "www.ad.nl",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
        "Cookie": 'pwv=2; pws=functional|analytics|content_recommendation|targeted_advertising|social_media; pwv=2; pws=functional|analytics|content_recommendation|targeted_advertising|social_media; _ga=GA1.2.1757703062.1574304025; _gid=GA1.2.780524530.1574304025; _hjid=ded29692-38b1-496b-b893-17c6581cbb66; __gads=ID=bd7481580501f9c2:T=1574304026:S=ALNI_MZblFlDcYwoLiRX3SlZ64IIHSxL8A; cX_S=k383z9wp11hp7mvn; cX_P=k383z9wqtc43fc9c; kntRedirect=true; lastConsentChange=1574304052874; DPGconsent=BOqW7wQOqW7wQADABAENCv-AAAAst6_-eauaxo25_P7J9kRlAL6lgRrPyFAQKQAM4AeCJWBiKgUkyDUoCUEIAoRAAERATCJARJgQEAESgAuAAJAgAwCAAAAIBAAAAAAABAAQAAAAAAAAAAAAAAAA; _sotmpid=0:k383zmza:yhMxSuLpbu0U1Y17Z282xj_puCOWPpCz; gig_bootstrap_3_P5Nmq7DTo9xh8yVx5Vm74AVQEL4g1C_-STsGxC2efKVKj2r-GzbIyzUltSXtTo5v=accounts; kppid_managed=M8ToJRCu; _gcl_au=1.1.99817512.1574304108; __gfp_64b=NccVNAGpvLt4e8UMDCmN0Uo.W9euo7N3qAm4erwiR2f.l7; _ain_uid=1574304376685.18606700.303829495; PushSubscriberStatus=CLOSED; peclosed=true; has_js=1; temptationTrackingId="bAnTEQnVS_i-cwYvsenUrQ=="; cstp=1; _sp_ses.b303=*; lastRegioSection=friesland; _sotmsid=0:k38backc:Ad3MyMoguss82CaGH6xkMLFYjclA9LND; _ain_cid=1574317701038.648141649.9940084; _vwo_uuid_v2=D2F59D211A9179A8683E099C4328D86F2|cb8b6d7e72405486974ca0273f39516e; _gat_UA-47135003-7=1; _sp_id.b303=12e88bf3-8cae-48b2-b7c5-d8688305df70.1574304044.2.1574317993.1574307246.4a4aaa64-f580-4627-a90f-94af7867a641; MetrixLab_help=1; _polar_tu=*_%22mgtn%22_@2Q_u_@_79096db2-1b08-48d8-8ac9-5ff78a27fe8e_Q_n_@3Q_s_@2Q_sc_@*_v_@5Q_a_@20+Q_ss_@_%22q1b1nv_Q_sl_@_%22q1b3ji_Q_sd_@*+Q_v_@_5%5Bd6e5c94_Q_vc_@*_e_@2+Q_vs_@_%22q1b3jh_Q_vl_@_%22q1b3jh_Q_vd_@*+Q_vu_@_5f34fc7556e0b2b0fb9ed1fa80e17a79_Q_vf_@_%22k38ca4k7_+; GED_PLAYLIST_ACTIVITY=W3sidSI6Ik83RjMiLCJ0c2wiOjE1NzQzMTgwMTAsIm52IjowLCJ1cHQiOjE1NzQzMTc3MDAsImx0IjoxNTc0MzE3NzI2fV0.'
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

    def make_requests_from_url(self, url):
        return FormRequest(url, dont_filter=True,headers=self.headers)

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

