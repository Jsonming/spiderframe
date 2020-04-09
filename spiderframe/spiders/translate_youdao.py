# -*- coding: utf-8 -*-
import scrapy
from spiderframe.items import SpiderframeItem
from scrapy_redis.spiders import RedisSpider


class TranslateYoudaoSpider(RedisSpider):
    name = 'translate_youdao'
    allowed_domains = ['dict.youdao.com']
    redis_key = 'youdao_word_urls'
    custom_settings = {
        'DOWNLOAD_DELAY': '0.1',
        'REDIS_HOST': '123.56.11.156',
        'REDIS_PORT': 8888,
        'REDIS_PARAMS': {
            'password': '',
            'db': 0
        },
    }

    # def start_requests(self):
    #     with open(r'D:\Workspace\workspace\work\English_word\lower_word.txt', 'r', encoding='utf8')as f:
    #         for key_word in f.readlines()[:1]:
    #             keyword = key_word.strip().split()[0]
    #             start_url = 'http://dict.youdao.com/w/{}/'.format(keyword)
    #             yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True)


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
            pronounce = response.xpath('//div[@class="baav"]/span[@class="pronounce"]')  # 抓取读音
            en_phonetic, am_phonetic, un_phonetic = '', '', ''
            if pronounce:
                for item in pronounce:
                    pronounce_lang = item.xpath("./text()").extract()  # 根据标签区分英式和美式
                    if pronounce_lang:
                        pronounce_text = ''.join(pronounce_lang).strip()
                        pronounce_text = pronounce_text.replace(" '", '').replace("’", '')
                        if pronounce_text == "英":
                            en_phonetic = ''.join(item.xpath('./span[@class="phonetic"]/text()').extract())
                        elif pronounce_text == "美":
                            am_phonetic = ''.join(item.xpath('./span[@class="phonetic"]/text()').extract())
                        else:
                            un_phonetic = ''.join(item.xpath('./span[@class="phonetic"]/text()').extract())

            item = SpiderframeItem()
            item['title'] = word  # title  字段 存单词
            item['category'] = word_tag[0]  # category 存显示的单词
            item['content'] = en_phonetic  # content 字段存 英式英语
            item['item_name'] = am_phonetic  # item_name 字段  美式英语
            item['item_id'] = un_phonetic  # item_id 字段  不确定是英式还是美式的情况
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
