# -*- coding: utf-8 -*-
import scrapy
import re
import json
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon


class TranslateIcibaSpider(scrapy.Spider):
    name = 'translate_iciba'
    allowed_domains = ['www.iciba.com']
    start_urls = ['http://www.iciba.com/']
    custom_settings = {
        "DOWNLOAD_DELAY": 0.3
    }

    def start_requests(self):
        ssdb_con = SSDBCon().connection()
        for i in range(200000):
            item = ssdb_con.lpop("iciba_word_urls")
            keyword = item.decode("utf8")
            url = "http://www.iciba.com/word?w={}".format(keyword)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        json_data_string = re.findall('<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
                                      response.text)
        if json_data_string:
            json_data = json.loads(json_data_string[0])
            base_info = json_data.get("props", {}).get("initialDvaState", {}).get("word", {}).get("wordInfo", {}).get(
                "baesInfo", {})
            word_name = base_info.get("word_name", "")
            ph_en_l = base_info.get("symbols", [])
            if ph_en_l:
                ph_en = ph_en_l[0].get("ph_en", "")  # 英式读音
            else:
                ph_en = ""
            ph_am_l = base_info.get("symbols", [])
            if ph_am_l:
                ph_am = ph_am_l[0].get("ph_am", "")  # 美式读音
            else:
                ph_am = ""
            ph_other_l = base_info.get("symbols", [])
            if ph_other_l:
                ph_other = ph_other_l[0].get("ph_other", "")  # 其他读音
            else:
                ph_other = ""

            item = SpiderframeItem()
            item['title'] = response.meta.get("keyword")  # title  字段 存单词
            item['category'] = word_name  # category 存显示的单词  google没有跳转现实
            item['content'] = ph_en  # content 字段存 英式英语
            item['item_name'] = ph_am  # category 字段  美式英语
            item['item_id'] = ph_other  # 显示其他字段
            return item
