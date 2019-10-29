# -*- coding: utf-8 -*-
import re
import json
import scrapy
from spiderframe.script.baidu_translate_js import BaiDuTranslateJS
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem

oxford_sentence_dict = []
usecase_sentence_dict = []


class TranslateBaiduSpider(scrapy.Spider):
    name = 'translate_baidu'
    allowed_domains = ['fanyi.baidu.com/translate']
    start_urls = ['http://www.baidu.com']

    def start_requests(self):
        url = 'http://fanyi.baidu.com/translate/'
        with open(r'D:\datatang\spiderframe\spiderframe\files\简单句单词总.txt', 'r', encoding='utf8')as f:
            for key_word in f:
                keyword = key_word.strip()
                yield scrapy.Request(url=url, meta={"query": keyword}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        windows_gtk = re.findall(";window.gtk = (.*?);</script>", response.text)[0][1:-1]
        token = re.findall(r"token: '(.*?)',", response.text)[0]
        query = response.meta.get("query")

        node = BaiDuTranslateJS()
        sign = node.get_sign(query, windows_gtk)

        url = "https://fanyi.baidu.com/v2transapi"
        data = {
            'from': 'en',
            'to': "zh",
            "query": query,
            "transtype": 'translang',
            "simple_meas_flag": '3',
            "sign": sign,
            'token': token
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_item, dont_filter=True,
                                 meta={"keyword": query})

    def parse_item(self, response):
        json_data = json.loads(response.text)
        dr = re.compile(r'<[^>]+>', re.S)

        dict_result = json_data.get("dict_result", {})

        # 英译英
        edict = dict_result.get("edict")
        if edict:
            tr_groups = edict.get("item")
            sentences = [item for tr_group in tr_groups for example in tr_group.get("tr_group") for item in
                         example.get("example")]
            for example_sentence in sentences:
                if example_sentence:
                    md = md5(example_sentence)
                    item = SpiderframeItem()
                    item['content'] = example_sentence
                    item['title'] = response.meta.get("keyword")
                    item['category'] = 'baidu'
                    item['item_id'] = md
                    yield item

        # 柯林斯
        collins = dict_result.get("collins")
        if collins:
            entry = collins.get("entry")
            if entry:
                for item_info in entry:
                    value = item_info.get("value")
                    for value_info in value:
                        word_def = value_info.get("def")
                        if word_def:
                            example_sentence = dr.sub('', word_def).strip()
                            if example_sentence:
                                md = md5(example_sentence)
                                item = SpiderframeItem()
                                item['content'] = example_sentence
                                item['title'] = response.meta.get("keyword")
                                item['category'] = 'baidu'
                                item['item_id'] = md
                                yield item

                        mean_type = value_info.get("mean_type")
                        if mean_type:
                            for example_info in mean_type:
                                example = example_info.get("example")
                                if example:
                                    collins_sentence = example[0].get("ex").replace("...", '')
                                    collins_s = dr.sub('', collins_sentence).strip()
                                    md = md5(collins_s)
                                    item = SpiderframeItem()
                                    item['content'] = collins_s
                                    item['title'] = response.meta.get("keyword")
                                    item['category'] = 'baidu'
                                    item['item_id'] = md
                                    yield item

        # 牛津
        oxford = dict_result.get("oxford")
        if oxford:
            data = oxford.get("entry")[0].get("data")
            TranslateBaiduSpider.find_data(data)
            global oxford_sentence_dict
            oxford_sentences = [item.get("enText") for item in oxford_sentence_dict]

            for example_sentence in oxford_sentences:
                if example_sentence:
                    md = md5(example_sentence)
                    item = SpiderframeItem()
                    item['content'] = example_sentence
                    item['title'] = response.meta.get("keyword")
                    item['category'] = 'baidu'
                    item['item_id'] = md
                    yield item

        # 同义词辨析
        synonym = dict_result.get("synonym")
        if synonym:
            synonyms = synonym[0].get("synonyms")
            for syn in synonyms:
                for item in syn.get("ex"):
                    example_sentence = item.get("enText")
                    if example_sentence:
                        md = md5(example_sentence)
                        item = SpiderframeItem()
                        item['content'] = example_sentence
                        item['title'] = response.meta.get("keyword")
                        item['category'] = 'baidu'
                        item['item_id'] = md
                        yield item

                    # 词语用例
        usecase = dict_result.get("usecase")
        if usecase:
            use_case_data = usecase.get("idiom")
            TranslateBaiduSpider.use_case_data(use_case_data)
            global usecase_sentence_dict
            for case in usecase_sentence_dict:
                example_sentence = case.get("enText")
                if example_sentence:
                    md = md5(example_sentence)
                    item = SpiderframeItem()
                    item['content'] = example_sentence
                    item['title'] = response.meta.get("keyword")
                    item['category'] = 'baidu'
                    item['item_id'] = md
                    yield item

        liju = json_data.get("liju_result", {})

        # 双语例句
        double_sentence_string = liju.get("double")
        if double_sentence_string:
            double_sentences = json.loads(double_sentence_string)
            for double_item in double_sentences:
                double_sentence_list = double_item[0]
                example_sentence = ''.join(
                    [item[0] + item[-1] if len(item) == 5 else item[0] for item in double_sentence_list])
                if example_sentence:
                    md = md5(example_sentence)
                    item = SpiderframeItem()
                    item['content'] = example_sentence
                    item['title'] = response.meta.get("keyword")
                    item['category'] = 'baidu'
                    item['item_id'] = md
                    yield item

        # 单例句
        single_sentence_string = liju.get("single")
        if single_sentence_string:
            single_sentences = json.loads(single_sentence_string)
            for single_item in single_sentences:
                single_sentence_list = single_item[0]
                example_sentence = ''.join(
                    [item[0] + item[-1] if len(item) == 4 else item[0] for item in single_sentence_list])
                if example_sentence:
                    md = md5(example_sentence)
                    item = SpiderframeItem()
                    item['content'] = example_sentence
                    item['title'] = response.meta.get("keyword")
                    item['category'] = 'baidu'
                    item['item_id'] = md
                    yield item

    @staticmethod
    def find_data(data):
        """
            提取牛津词典中的例句json
        :param json_data:
        :return:
        """
        global oxford_sentence_dict
        if isinstance(data, dict):
            if data.get("tag") == "x":
                oxford_sentence_dict.append(data)
            else:
                for _, item in data.items():
                    TranslateBaiduSpider.find_data(item)
        elif isinstance(data, list):
            for item in data:
                TranslateBaiduSpider.find_data(item)
        else:
            pass

    @staticmethod
    def use_case_data(data):
        """
            提取用户用例中的例句json
        :param json_data:
        :return:
        """
        global usecase_sentence_dict
        if isinstance(data, dict):
            if data.get("tag") == "x":
                usecase_sentence_dict.append(data)
            else:
                for _, item in data.items():
                    TranslateBaiduSpider.use_case_data(item)
        elif isinstance(data, list):
            for item in data:
                TranslateBaiduSpider.use_case_data(item)
        else:
            pass
