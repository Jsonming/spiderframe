#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 17:22
# @Author  : yangmingming
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from scrapy import cmdline

cmdline.execute("scrapy crawl image_google -a category=猫".split())