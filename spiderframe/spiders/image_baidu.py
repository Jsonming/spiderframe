# -*- coding: utf-8 -*-
import re
import scrapy
import json
from spiderframe.items import ImgsItem
from urllib.parse import quote


class ImageBaiduSpider(scrapy.Spider):
    name = 'image_baidu'

    def __init__(self, category="狗", *args, **kwargs):
        super(ImageBaiduSpider, self).__init__(*args, **kwargs)
        self.category = category

    def start_requests(self):
        for j in range(0, 30, 30):
            # url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={category}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=3&ic=&hd=&latest=&copyright=&word={category}&s=&se=&tab=&width=0&height=0&face=&istype=&qc=&nc=&fr=&expermode=&force=&pn={j}&rn=30&gsm=5a&78&1564382012654=".format(category=quote(self.category),j=j)
            url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={category}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=9&ic=&hd=1&latest=0&copyright=0&word={category}&s=&se=&tab=&width=0&height=0&face=&istype=&qc=&nc=&fr=&expermode=&force=&pn={j}&rn=30&gsm=1a4&1564384419589=".format(
                category=quote(self.category), j=j)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp = json.loads(response.text)
        data = resp.get("data", [])

        for img in data:
            pageNum = img.get("pageNum")
            di = img.get("di")
            cs = str(img.get("cs"))
            cs = cs.replace(",", "%2C")
            os = str(img.get("os"))
            os = os.replace(",", "%2C")
            simid = str(img.get("simid"))
            simid = simid.replace(",", "%2C")
            # true_url="https://image.baidu.com/search/detail?z=3&ipn=d&word=%E7%8C%AB&step_word=&hs=2&pn={pageNum}&spn=0&di={di}&pi=0&rn=1&tn=baiduimagedetail&is=0%2C0&istype=0&ie=utf-8&oe=utf-8&in=&cl=2&lm=-1&st=undefined&cs={cs}&os={os}&simid={simid}&adpicid=0&lpn=0&ln=1424&fr=&fmq=1564386638083_R&fm=&ic=undefined&s=undefined&hd=undefined&latest=undefined&copyright=undefined&se=&sme=&tab=0&width=0&height=0&face=undefined&ist=&jit=&cg=&bdtype=0&oriquery=&objurl={objurl}&fromurl={fromurl}&gsm=78&rpstart=0&rpnum=0&islist=&querylist=&force=undefined".format(pageNum=pageNum,di=di,cs=cs,os=os,simid=simid,objurl=objurl,fromurl=fromurl)
            true_url = "https://image.baidu.com/search/detail?z=3&ipn=d&word={category}&step_word=&hs=2&pn={pageNum}&spn=0&di={di}&pi=0&rn=1&tn=baiduimagedetail&is=0%2C0&istype=0&ie=utf-8&oe=utf-8&in=&cl=2&lm=-1&st=undefined&cs={cs}&os={os}&simid={simid}&adpicid=0&lpn=0&ln=1424&fr=&fmq=1564386638083_R&fm=&ic=undefined&s=undefined&hd=undefined&latest=undefined&copyright=undefined&se=&sme=&tab=0&width=0&height=0&face=undefined&ist=&jit=&cg=&bdtype=0&oriquery=&".format(
                category=quote(self.category), pageNum=pageNum, di=di, cs=cs, os=os, simid=simid)
            yield scrapy.Request(url=true_url, callback=self.parse_url, dont_filter=True)

    def parse_url(self, response):
        resp = response.text
        reg = r'src="(https://timgsa.baidu.com/timg.*?g.*?)"'
        imgre = re.compile(reg)
        img_list = re.findall(imgre, resp)
        item = ImgsItem()
        item["category"] = self.category
        item["image_urls"] = img_list
        yield item

        # total_num = resp.get("displayNum")
        # current_num = re.findall('&pn=(.*?)&rn=30', response.url)[0]
        # if int(current_num) < int(total_num):
        #     url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={category}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={category}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn={page}&rn=30&gsm=1e&1560505489300=".format(
        #         category=quote(self.category), page=int(current_num)+30)
        #     yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
