#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 18:16
# @Author  : yangmingming
# @Site    : 
# @File    : baidu_translate_js.py
# @Software: PyCharm
import execjs
import os


class BaiDuTranslateJS(object):
    def __init__(self):
        path = os.path.abspath(os.path.dirname(__file__))

        with open(os.path.join(path, "baidufanyi.js"), "r", encoding="utf-8") as f:
            js_string = f.read()
            self.sign_js = execjs.compile(js_string)

    def get_sign(self, query, gtk):
        sign_js = 'e("{query}", "{gtk}")'.format(**locals())
        return self.sign_js.eval(sign_js)


if __name__ == '__main__':
    bd = BaiDuTranslateJS()
    print(bd.get_sign(query="know", gtk='320305.131321201'))
