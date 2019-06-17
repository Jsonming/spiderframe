# -*- coding: utf-8 -*-
import scrapy
from spiderframe.download import you_get_download


class VideoQuanminSpider(scrapy.Spider):
    name = 'video_quanmin'
    allowed_domains = ['quanmin.baidu.com']
    start_urls = [
        'https://quanmin.hao222.com/sv?source=share-h5&pd=feed&vid=10467990803470971858&shared_cuid=0aS88jaF2u_Lav8ZgaBSiguzvig1iSailuvzuYai2il68v8Jgi-_ajfsSO5jfSPurIFmA&shared_uid=Yu2O8_a5vfsOA']

    def parse(self, response):
        you_get_download(
            "https://quanmin.hao222.com/sv?source=share-h5&pd=qm_share_mvideo&vid=4734903240846954699&shared_cuid=givSajuoS8g1uvfglu-Sf0ihSa_m8HaI0uvef0aQSaiiav8FYPBgi_uovi_Ra2t1A")
