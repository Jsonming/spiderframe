#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 10:50
# @Author  : yangmingming
# @Site    : 
# @File    : common.py
# @Software: PyCharm
import hashlib


def md5(string):
    """ 对字符串做md5"""
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()
