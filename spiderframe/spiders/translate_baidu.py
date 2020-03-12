# -*- coding: utf-8 -*-
import re
import json
import scrapy
from spiderframe.script.baidu_translate_js import BaiDuTranslateJS
from spiderframe.common.common import md5
from spiderframe.items import SpiderframeItem
from spiderframe.common.db import SSDBCon

oxford_sentence_dict = []
usecase_sentence_dict = []


class TranslateBaiduSpider(scrapy.Spider):
    name = 'translate_baidu'
    allowed_domains = ['fanyi.baidu.com/translate']
    start_urls = ['http://www.baidu.com']
    custom_setting = {
        "DOWNLOAD_DELAY": 2
    }

    def start_requests(self):
        url = 'http://fanyi.baidu.com/translate/'

        # with open(r'D:\Workspace\spiderframe\spiderframe\files\commen_words.txt', 'r', encoding='utf8')as f:
        #     for key_word in f.readlines()[53192:100000]:
        #         keyword = key_word.strip()
        #         yield scrapy.Request(url=url, meta={"query": keyword}, callback=self.parse, dont_filter=True)
        #
        # keyword = "seriess"
        # yield scrapy.Request(url=url, meta={"query": keyword}, callback=self.parse, dont_filter=True)

        ssdb_con = SSDBCon().connection()
        for i in range(1000):
            item = ssdb_con.lpop("baidu_word_urls")
            keyword = item.decode("utf8")
            yield scrapy.Request(url=url, meta={"query": keyword}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # windows_gtk = re.findall(";window.gtk = (.*?);</script>", response.text)[0][1:-1]
        # token = re.findall(r"token: '(.*?)',", response.text)[0]

        windows_gtk = '320305.131321201'
        token = "801c121315094c2f0451845bea9ce2fe"
        query = response.meta.get("query")

        node = BaiDuTranslateJS()
        sign = node.get_sign(query, windows_gtk)

        url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
        data = {
            'from': 'en',
            'to': "zh",
            "query": query,
            "transtype": 'translang',
            "simple_meas_flag": '3',
            "sign": sign,
            'token': token
        }
        header = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cache-control": "no-cache",
            "cookie": "BAIDUID=02725590C792FF940E803CB07B053FEA:"
                      "FG=1; BIDUPSID=02725590C792FF940E803CB07B053FEA; "
                      "PSTM=1557990196; "
                      "to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; "
                      "REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; HISTORY_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; H_PS_PSSID=1445_21097_29921_29568_29220_26350; delPer=0; PSINO=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1572508074,1572512679,1572512867,1572515669; yjs_js_security_passport=75fbfb6eb5e8b93053fdda8c6f15e8160a536f70_1572515753_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1572516236; __yjsv5_shitong=1.0_7_5c003f5356b4428943d8f74bb6c658efd893_300_1572516236513_123.58.106.254_79b85b3f"
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_item, dont_filter=True, headers=header,
                                 meta={"keyword": query})

    def parse_item(self, response):
        json_data = json.loads(response.text)
        dr = re.compile(r'<[^>]+>', re.S)
        word = response.meta.get("keyword")

        dict_result = json_data.get("dict_result", {})
        try:
            ph_en = dict_result.get("simple_means", {}).get("symbols")[0].get("ph_en")
        except Exception as e:
            ph_en = ""

        try:
            ph_am = dict_result.get("simple_means", {}).get("symbols")[0].get("ph_am")
        except Exception as e:
            ph_am = ""

        item = SpiderframeItem()
        item['title'] = word  # title  字段 存单词
        item['category'] = word  # category 存显示的单词
        item['content'] = ph_en  # content 字段存 英式英语
        item['item_name'] = ph_am  # category 字段  美式英语
        yield item


        # print(ph_en, ph_am)
        # with open(r'D:\Workspace\spiderframe\spiderframe\files\baidu_phonetic.txt', 'a', encoding='utf8')as f:
        #     f.write(response.meta.get("keyword") + '\t' + ph_en + '\t' + ph_am + "\n")

        # 英译英
        # edict = dict_result.get("edict")
        # if edict:
        #     tr_groups = edict.get("item")
        #     sentences = [item for tr_group in tr_groups for example in tr_group.get("tr_group") for item in
        #                  example.get("example")]
        #     for example_sentence in sentences:
        #         if example_sentence:
        #             md = md5(example_sentence)
        #             item = SpiderframeItem()
        #             item['content'] = example_sentence
        #             item['title'] = response.meta.get("keyword")
        #             item['category'] = 'baidu'
        #             item['item_id'] = md
        #             yield item
        #
        # 柯林斯
        # collins = dict_result.get("collins")
        # if collins:
        #     entry = collins.get("entry")
        #     if entry:
        #         for item_info in entry:
        #             value = item_info.get("value")
        #             for value_info in value:
        #                 word_def = value_info.get("def")
        #                 if word_def:
        #                     example_sentence = dr.sub('', word_def).strip()
        #                     if example_sentence:
        #                         md = md5(example_sentence)
        #                         item = SpiderframeItem()
        #                         item['content'] = example_sentence
        #                         item['title'] = response.meta.get("keyword")
        #                         item['category'] = 'baidu'
        #                         item['item_id'] = md
        #                         yield item
        #
        #                 mean_type = value_info.get("mean_type")
        #                 if mean_type:
        #                     for example_info in mean_type:
        #                         example = example_info.get("example")
        #                         if example:
        #                             collins_sentence = example[0].get("ex").replace("...", '')
        #                             collins_s = dr.sub('', collins_sentence).strip()
        #                             md = md5(collins_s)
        #                             item = SpiderframeItem()
        #                             item['content'] = collins_s
        #                             item['title'] = response.meta.get("keyword")
        #                             item['category'] = 'baidu'
        #                             item['item_id'] = md
        #                             yield item
        #
        # 牛津
        # oxford = dict_result.get("oxford")
        # if oxford:
        #     data = oxford.get("entry")[0].get("data")
        #     TranslateBaiduSpider.find_data(data)
        #     global oxford_sentence_dict
        #     oxford_sentences = [item.get("enText") for item in oxford_sentence_dict]
        #
        #     for example_sentence in oxford_sentences:
        #         if example_sentence:
        #             md = md5(example_sentence)
        #             item = SpiderframeItem()
        #             item['content'] = example_sentence
        #             item['title'] = response.meta.get("keyword")
        #             item['category'] = 'baidu'
        #             item['item_id'] = md
        #             yield item
        #
        # 同义词辨析
        # synonym = dict_result.get("synonym")
        # if synonym:
        #     synonyms = synonym[0].get("synonyms")
        #     for syn in synonyms:
        #         for item in syn.get("ex"):
        #             example_sentence = item.get("enText")
        #             if example_sentence:
        #                 md = md5(example_sentence)
        #                 item = SpiderframeItem()
        #                 item['content'] = example_sentence
        #                 item['title'] = response.meta.get("keyword")
        #                 item['category'] = 'baidu'
        #                 item['item_id'] = md
        #                 yield item
        #
        #             词语用例
        # usecase = dict_result.get("usecase")
        # if usecase:
        #     use_case_data = usecase.get("idiom")
        #     TranslateBaiduSpider.use_case_data(use_case_data)
        #     global usecase_sentence_dict
        #     for case in usecase_sentence_dict:
        #         example_sentence = case.get("enText")
        #         if example_sentence:
        #             md = md5(example_sentence)
        #             item = SpiderframeItem()
        #             item['content'] = example_sentence
        #             item['title'] = response.meta.get("keyword")
        #             item['category'] = 'baidu'
        #             item['item_id'] = md
        #             yield item
        #
        # liju = json_data.get("liju_result", {})
        #
        # 双语例句
        # double_sentence_string = liju.get("double")
        # if double_sentence_string:
        #     double_sentences = json.loads(double_sentence_string)
        #     for double_item in double_sentences:
        #         double_sentence_list = double_item[0]
        #         example_sentence = ''.join(
        #             [item[0] + item[-1] if len(item) == 5 else item[0] for item in double_sentence_list])
        #         if example_sentence:
        #             md = md5(example_sentence)
        #             item = SpiderframeItem()
        #             item['content'] = example_sentence
        #             item['title'] = response.meta.get("keyword")
        #             item['category'] = 'baidu'
        #             item['item_id'] = md
        #             yield item
        #
        # 单例句
        # single_sentence_string = liju.get("single")
        # if single_sentence_string:
        #     single_sentences = json.loads(single_sentence_string)
        #     for single_item in single_sentences:
        #         single_sentence_list = single_item[0]
        #         example_sentence = ''.join(
        #             [item[0] + item[-1] if len(item) == 4 else item[0] for item in single_sentence_list])
        #         if example_sentence:
        #             md = md5(example_sentence)
        #             item = SpiderframeItem()
        #             item['content'] = example_sentence
        #             item['title'] = response.meta.get("keyword")
        #             item['category'] = 'baidu'
        #             item['item_id'] = md
        #             yield item
    #
    # @staticmethod
    # def find_data(data):
    #     """
    #         提取牛津词典中的例句json
    #     :param json_data:
    #     :return:
    #     """
    #     global oxford_sentence_dict
    #     if isinstance(data, dict):
    #         if data.get("tag") == "x":
    #             oxford_sentence_dict.append(data)
    #         else:
    #             for _, item in data.items():
    #                 TranslateBaiduSpider.find_data(item)
    #     elif isinstance(data, list):
    #         for item in data:
    #             TranslateBaiduSpider.find_data(item)
    #     else:
    #         pass
    #
    # @staticmethod
    # def use_case_data(data):
    #     """
    #         提取用户用例中的例句json
    #     :param json_data:
    #     :return:
    #     """
    #     global usecase_sentence_dict
    #     if isinstance(data, dict):
    #         if data.get("tag") == "x":
    #             usecase_sentence_dict.append(data)
    #         else:
    #             for _, item in data.items():
    #                 TranslateBaiduSpider.use_case_data(item)
    #     elif isinstance(data, list):
    #         for item in data:
    #             TranslateBaiduSpider.use_case_data(item)
    #     else:
    #         pass
