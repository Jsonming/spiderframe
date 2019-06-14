# -*- coding: utf-8 -*-
import scrapy
from spiderframe.download import pytube_download


class VideoYoutubeSpider(scrapy.Spider):
    name = 'video_youtube'
    allowed_domains = ['www.youtube.com']
    start_urls = ['https://www.youtube.com/watch?v=N_DCZ0I0gv4']

    # def parse(self, response):
    #     pool.map(pytube_download, ['https://www.youtube.com/watch?v=N_DCZ0I0gv4'])
