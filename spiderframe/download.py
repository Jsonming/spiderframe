#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 14:21
# @Author  : yangmingming
# @Site    : 
# @File    : download.py
# @Software: PyCharm
import os
import sys

import you_get
from pytube import YouTube

from . import settings


def you_get_download(url=None, path=None):
    """
        调用you-get 抓取视频
    :param url: 视频url
    :param path: 存储路径
    :return:
    """
    if not path:
        path = '/data/video/video'
    else:
        path = './files/video/{}'.format(path)
    if not os.path.exists(path):
        os.makedirs(path)

    sys.argv = ['you-get', '-o', path, url]
    you_get.main()


def pytube_download(url=None, path=None):
    """
        youtube专用下载器，NB的地方在于如果有字幕流，可以下载字幕， 与you_get相同有音频流可以下载音频
    :param url: 视频url
    :param path: 存储路径
    :return:
    """
    if not path:
        path = './files/video'
    if not os.path.exists(path):
        os.makedirs(path)
    YouTube(url).streams.first().download(path)


def googel_img_download(word=None, path=None, limit=None):
    """
        谷歌图片下载器
    :param keyword:
    :param path:
    :param limit:
    :return:
    """
    image_store = settings.IMAGES_STORE
    command = 'googleimagesdownload -k {} -o {} -l 10  --chromedriver="D:\chromedriver_win32"'.format(word, image_store)
    os.system(command)
