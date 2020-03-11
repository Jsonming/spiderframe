# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class TranslateYoudaoSpider(RedisSpider):
    name = 'translate_youdao'
    allowed_domains = ['dict.youdao.com']
    redis_key = 'youdao_word_urls'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    def start_requests(self):
        with open(r'D:\Workspace\workscript\work_script\demo.txt', 'r', encoding='utf8')as f:
            for key_word in f.readlines()[:1]:
                keyword = key_word.strip().split()[0]
                start_url = 'http://dict.youdao.com/w/{}/'.format(keyword)
                yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # 验证单词是否合法
        # word_tag = response.xpath('//h2[@class="wordbook-js"]/span/text()').extract()
        # if word_tag:
        #     item = SpiderframeItem()
        #     item['content'] = word_tag
        #     item['category'] = 'youdao'
        #     item["title"] = ''
        #     item["url"] = response.url
        #     yield item

        # 抓取音标
        word = response.url.split("/")[-2]  # 原始单词
        word_tag = response.xpath('//h2[@class="wordbook-js"]/span/text()').extract()  # 显示单词
        if word_tag:
            pronounce = response.xpath('//div[@class="baav"]/span[@class="pronounce"]')  # 要求英音美音区分开，不采用循环的方式
            en_phonetic, am_phonetic = '', ''
            if len(pronounce) == 2:
                e_phonetic = pronounce[0].xpath('./span[@class="phonetic"]/text()').extract()
                if e_phonetic:
                    en_phonetic = e_phonetic[0]  # 有英音

                a_phonetic = pronounce[1].xpath('./span[@class="phonetic"]/text()').extract()
                if a_phonetic:
                    am_phonetic = a_phonetic[0]  # 有美音

            item = SpiderframeItem()
            item['title'] = word  # title  字段 存单词
            item['category'] = word_tag[0]  # category 存显示的单词
            item['content'] = en_phonetic  # content 字段存 英式英语
            item['item_name'] = am_phonetic  # category 字段  美式英语
            yield item

        # 抓取例句
        # examples = response.xpath('//div[@class="examples"]/p[1]/text()').extract()
        # dr = re.compile(r'<[^>]+>', re.S)
        #
        # if examples:
        #     for example in examples:
        #         collins_sentence = example.replace("...", '')
        #         collins_s = dr.sub('', collins_sentence).strip()
        #         md = md5(collins_s)
        #         item = SpiderframeItem()
        #         item['content'] = collins_s
        #         item['title'] = response.meta.get("keyword")
        #         item['category'] = 'youdao'
        #         item['item_id'] = md
        #         yield item
        #
        # examplesToggle = response.xpath('//div[@id="examplesToggle"]/div/ul/li/p[1]')
        # if examplesToggle:
        #     for p_node in examplesToggle:
        #         p_node_str = ''.join(p_node.xpath('.//text()').extract()).strip()
        #         collins_sentence = p_node_str.replace("...", '')
        #         collins_s = dr.sub('', collins_sentence).strip()
        #         md = md5(collins_s)
        #         item = SpiderframeItem()
        #         item['content'] = collins_s
        #         item['title'] = response.meta.get("keyword")
        #         item['category'] = 'youdao'
        #         item['item_id'] = md
        #         yield item
