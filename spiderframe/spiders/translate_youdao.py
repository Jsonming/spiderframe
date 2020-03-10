# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from spiderframe.items import SpiderframeItem


class TranslateYoudaoSpider(RedisSpider):
    name = 'translate_youdao'
    allowed_domains = ['dict.youdao.com']
    redis_key = 'words'
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
        with open(r'D:\Workspace\spiderframe\spiderframe\files\commen_words.txt', 'r', encoding='utf8')as f:
            for key_word in f.readlines()[:5]:
                keyword = key_word.strip().split("\t")[0]
                start_url = 'http://dict.youdao.com/w/{}/'.format(keyword)
                yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True, meta={"keyword": keyword})

    def parse(self, response):
        # 验证单词是否合法
        word_tag = response.xpath('//h2[@class="wordbook-js"]/span/text()').extract()
        if word_tag:
            item = SpiderframeItem()
            item['content'] = word_tag
            item['category'] = 'youdao'
            item["title"] = ''
            item["url"] = response.url
            yield item

        # 抓取音标
        # ph = []
        # ph.append(response.meta.get("keyword"))
        # phonetics = response.xpath('//div[@class="baav"]/span[@class="pronounce"]')
        # for item in phonetics:
        #     phonetic_text = item.xpath('./text()').extract()
        #     phonetic_text = ''.join(phonetic_text).strip()
        #     phonetic = item.xpath('./span[@class="phonetic"]/text()').extract()
        #     phonetic = ''.join(phonetic).strip()
        #     ph.append(phonetic)
        # if phonetic_text == "英":
        #     ph.append(phonetic)

        # with open(r'D:\Workspace\spiderframe\spiderframe\files\lower_phonetic.txt', 'a', encoding='utf8')as f:
        #     f.write('\t'.join(ph) + "\n")

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
