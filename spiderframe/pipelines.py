# -*- coding: utf-8 -*-

import hashlib
import os
import sys

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis
from scrapy.pipelines.images import ImagesPipeline

from spiderframe.items import ImgsItem
from spiderframe.spiders.Egypt_masrawy_content import EgyptMasrawyContentSpider
from spiderframe.spiders.English_corpus_genlib import EnglishCorpusGenlibSpider
from spiderframe.spiders.English_corpus_gutenberg_new import EnglishCorpusGutenbergNewSpider
from spiderframe.spiders.Greece_enet_content import GreeceEnetContentSpider
from spiderframe.spiders.Netherlands_nrc_content import NetherlandsNrcContentSpider
from spiderframe.spiders.translate_baidu import TranslateBaiduSpider
from spiderframe.spiders.translate_bing import TranslateBingSpider
from spiderframe.spiders.translate_cnki import TranslateCnkiSpider
from spiderframe.spiders.translate_collins import TranslateCollinsSpider
from spiderframe.spiders.translate_dict import TranslateDictSpider
from spiderframe.spiders.translate_google import TranslateGoogleSpider
from spiderframe.spiders.translate_iciba import TranslateIcibaSpider
from spiderframe.spiders.translate_oxfordlearners import TranslateOxfordlearnersSpider
from spiderframe.spiders.translate_webster import TranslateWebsterSpider
from spiderframe.spiders.translate_youdao import TranslateYoudaoSpider
from spiderframe.spiders.translate_ldoceonline import TranslateLdoceonlineSpider
from spiderframe.spiders.translate_dictionary import TranslateDictionarySpider
from spiderframe.spiders.translate_macmillan import TranslateMacmillanSpider
from spiderframe.spiders.translate_cambridage import TranslateCambridageSpider
from . import settings


class SpiderframePipeline(object):
    def __init__(self):
        folder = os.path.dirname(__file__) + '/files/text'
        if not os.path.exists(folder):
            os.makedirs(folder)

    def process_item(self, item, spider):
        def save_text(string):
            file = './files/text/{}.txt'.format(spider.name)
            with open(file, 'a', encoding='utf8')as f:
                f.write(string + "\n")

        return item


class MySQLPipeline(object):
    def __init__(self):
        self.db_conn = None
        self.db_cur = None

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'malaysia')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        password = spider.settings.get('MYSQL_PASSWORD', '123456')
        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=password, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def insert_db(self, table_name, item):
        values = (
            item['url'],
            item['content'],
        )

        sql = 'INSERT INTO {db_name}(url, content) VALUES(%s,%s)'.format(db_name=table_name)  # 将表名设置为参数形式
        self.db_cur.execute(sql, values)
        self.db_conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, ImgsItem):
            # image_urls = item["image_urls"]
            # for url in image_urls:
            #     thumb_guid = hashlib.sha1(url.encode('utf8')).hexdigest()
            #     sql = 'INSERT INTO Img(img_name, url) VALUES(%s,%s)'
            #     self.db_cur.execute(sql, (thumb_guid, url))
            pass

        if isinstance(spider, GreeceEnetContentSpider):
            values = (
                item['url'],
                item['category'],
                item['title'],
                item['content'],
            )

            sql = 'INSERT INTO {db_name}(url,category,title,content) VALUES(%s,%s,%s,%s)'.format(
                db_name="Greece_enet_content")
            self.db_cur.execute(sql, values)
            self.db_conn.commit()

        if isinstance(spider, NetherlandsNrcContentSpider):
            values = (
                item['url'],
                item['category'],
                item['title'],
                item['content'],
            )

            sql = 'INSERT INTO {db_name}(url,category,title,content) VALUES(%s,%s,%s,%s)'.format(
                db_name="Netherlands_nrc_content")
            self.db_cur.execute(sql, values)
            self.db_conn.commit()

        if isinstance(spider, EgyptMasrawyContentSpider):
            values = (
                item['url'],
                item['category'],
                item['title'],
                item['content'],
            )

            sql = 'INSERT INTO {db_name}(url,category,title,content) VALUES(%s,%s,%s,%s)'.format(
                db_name="Egypt_masrawy_content")
            self.db_cur.execute(sql, values)
            self.db_conn.commit()

        if isinstance(spider, TranslateBaiduSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['title'],
                )
                sql = "update third_word_phonetic set baidu_show_word=%s,baidu_en_phonetic=%s,baidu_am_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateGoogleSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['title'],
                )
                sql = "update English_word_phonetic set google_show_word=%s,google_en_phonetic=%s,google_am_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateYoudaoSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['item_id'],
                    item['title'],
                )
                sql = "update third_word_phonetic set youdao_show_word=%s,youdao_en_phonetic=%s,youdao_am_phonetic=%s,youdao_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateIcibaSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['item_id'],
                    item['title'],
                )
                sql = "update second_word_phonetic set iciba_show_word=%s,iciba_en_phonetic=%s,iciba_am_phonetic=%s,iciba_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateOxfordlearnersSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['title'],
                )
                sql = "update second_word_phonetic set oxfordlearners_show_word=%s,oxfordlearners_en_phonetic=%s,oxfordlearners_am_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateWebsterSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item["item_id"],
                    item['title'],
                )
                sql = "update second_word_phonetic set webster_show_word=%s,webster_en_phonetic=%s,webster_am_phonetic=%s,webster_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateCollinsSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['item_id'],
                    item['title'],
                )
                sql = "update second_word_phonetic set collins_show_word=%s,collins_en_phonetic=%s,collins_am_phonetic=%s,collins_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateLdoceonlineSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['item_id'],
                    item['title'],
                )
                sql = "update second_word_phonetic set ldoceonline_show_word=%s,ldoceonline_en_phonetic=%s,ldoceonline_am_phonetic=%s,ldoceonline_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateDictionarySpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['item_id'],
                    item['title'],
                )
                sql = "update second_word_phonetic set dictionary_show_word=%s,dictionary_en_phonetic=%s,dictionary_am_phonetic=%s,dictionary_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateMacmillanSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['item_id'],
                    item['title'],
                )
                sql = "update second_word_phonetic set macmillan_show_word=%s,macmillan_en_phonetic=%s,macmillan_am_phonetic=%s,macmillan_uncertain_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateCambridageSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['title'],
                )
                sql = "update second_word_phonetic set cambridage_show_word=%s,cambridage_en_phonetic=%s,cambridage_am_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateBingSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['title'],
                )
                sql = "update English_word_phonetic set bing_show_word=%s,bing_en_phonetic=%s,bing_am_phonetic=%s where word=%s"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateDictSpider):
            if item:
                values = (
                    item['category'],
                    item['content'],
                    item['item_name'],
                    item['title'],
                )
                # sql = "update English_word_phonetic set dict_show_word=%s,dict_en_phonetic=%s,dict_am_phonetic=%s where word=%s"
                sql = "insert into Dict_word_phonetic (dict_phonetic_word,dict_en_phonetic,dict_am_phonetic,word) values (%s,%s,%s,%s)"
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, TranslateCnkiSpider):
            if item:
                values = (
                    item['category'],
                    item['title'],
                    item['item_id'],
                    item['content'],
                )
                sql = 'INSERT INTO {db_name}(source,word,md,sentence) VALUES(%s,%s,%s,%s)'.format(
                    db_name="translate_sentence_new")  # 将表名设置为参数形式
                self.db_cur.execute(sql, values)
                self.db_conn.commit()

        elif isinstance(spider, EnglishCorpusGutenbergNewSpider):
            self.insert_db("English_corpus_gutenberg", item)

        elif isinstance(spider, EnglishCorpusGenlibSpider):
            self.insert_db(spider.name, item)

        return item


class RedisPipeline(object):
    def __init__(self):
        self.db_conn = None
        self.fingerprint_key = 'fingerprint_temp'

    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 8888)
        db_index = spider.settings.get('REDIS_DB_INDEX', 0)
        self.db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index)

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

    def insert_db(self, db, item):
        self.db_conn.lpush(db, item)

    def insert_fingerprint(self, db, string):
        return self.db_conn.hset(name=db, key=string, value=1)

    def fingerprint_exist(self, db_name, string):
        return self.db_conn.hexists(name=db_name, key=string)

    def generate_fingerprint(self, string):
        md5 = hashlib.md5()
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()

    def check_url_crawled(self, content, fingerprint_key=None):
        if not fingerprint_key:
            fingerprint_key = self.fingerprint_key

        fingerprint = self.generate_fingerprint(content)
        if not self.fingerprint_exist(fingerprint_key, fingerprint):
            self.insert_fingerprint(fingerprint_key, fingerprint)
            return False
        else:
            print("指纹重复")
            return True

    def process_item(self, item, spider):
        if spider.name.endswith('link'):
            if not self.check_url_crawled(item['url']):
                self.insert_db(spider.name, item['url'])
        elif spider.name.endswith("content"):
            if not item['content']:
                self.insert_db(spider.name, item['url'])
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用的，其实这个方法本身就是去发送下载请求的
        request_objs = super(ImagePipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        path = super(ImagePipeline, self).file_path(request, response, info)
        category = request.item.get('category')
        image_store = settings.IMAGES_STORE
        category_path = os.path.join(image_store, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        # windows 平台和liunx平台分开
        if "win" in sys.platform:
            image_name = path.replace("full/", '')
            image_path = os.path.join(category_path, image_name)
        else:
            image_path = path.replace("full/", category + "/")
        return image_path
