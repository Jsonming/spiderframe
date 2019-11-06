#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 11:23
# @Author  : yangmingming
# @Site    :
# @File    : google_js.py
# @Software: PyCharm

import execjs


class Py4Js(object):

    def __init__(self):
        self.ctx = execjs.compile("""

         function a() {
         for (var a = {}, c = b.location.search.substring(1).split("&"), d = 0; d < c.length; d++) {
            var e = c[d].indexOf("=");
            if (-1 != e) {
                var h = c[d].substring(0, e);
                e = c[d].substring(e + 1);
                e = decodeURIComponent(e);
                a[h] = e
            }
        }
        return a
    }
    ;
        """)

    def get_tk(self, text):
        return self.ctx.call("a", text)


if __name__ == '__main__':
    tk = Py4Js()
    print(tk.get_tk("know"))
