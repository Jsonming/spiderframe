# -*- coding: utf-8 -*-
import re

import scrapy


class VideoDouyinLinkSpider(scrapy.Spider):
    name = 'video_douyin_link'
    allowed_domains = ['www.iesdouyin.com']
    start_urls = ['http://www.iesdouyin.com/']

    def __init__(self):
        self.user_id = '102220954116'  # 用户id配置
        self.dou_yin_id = '1212930875'  # id
        self._signature = '25QqnRAch2se8XIQmVB4z9uUKo'  # sign配置

    def start_requests(self):
        url = "https://www.iesdouyin.com/share/user/{}".format(self.user_id)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        dytk = re.search("dytk: '(.*?)'", response.text).group(1)
        nickname = re.search('<p class="nickname">(.*?)</p>', response.text).group(1)
        try:
            type = re.search('<span class="info">(.*?)</span>', response.text).group(1).replace(' ', '')
        except:
            type = ''
        url_detail = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?user_id={}&count=21&max_cursor=' \
                     '&aid=1128&_signature={}&dytk={}'.format(
            self.user_id, self._signature, dytk)
        yield scrapy.Request(url=url_detail, callback=self.parse_item)

    def parse_item(self, response):
        print(response.text)  # TODO 抖音没有打通， 以后专门抽时间解决
        # list = json.loads(response.text)['aweme_list']
        # has_more = json.loads(response.text)['has_more']
        #
        # for item in list:
        #     user_id = self.user_id
        #     title = item['desc']  # 读取视频名称
        #     try:
        #         video = item['video']['play_addr']['uri']
        #         video_url = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id={}".format(video)  # 拼接视频地址
        #     except KeyError:
        #         pass
