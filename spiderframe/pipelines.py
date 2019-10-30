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
from spiderframe.spiders.vietnam_news_vn_link import VietnamNewsVnLinkSpider
from spiderframe.spiders.video_bilibili_link import VideoBilibiliLinkSpider
from spiderframe.spiders.video_baidu_link import VideoBaiduLinkSpider
from spiderframe.spiders.vietnam_news_vn_content import VietnamNewsVnContentSpider
from spiderframe.spiders.vietnam_speaking_sentence import VietnamSpeakingSentenceSpider
from spiderframe.spiders.china_news_people_content import ChinaNewsPeopleContentSpider
from spiderframe.spiders.english_speaking_ted_link import EnglishSpeakingTedLinkSpider
from spiderframe.spiders.china_speechocean_link import ChinaSpeechoceanLinkSpider
from spiderframe.spiders.hebrew_walla_content import HebrewWallaContentSpider
from spiderframe.spiders.translate_google import TranslateGoogleSpider
from spiderframe.spiders.translate_baidu import TranslateBaiduSpider
from spiderframe.spiders.translate_youdao import TranslateYoudaoSpider
from spiderframe.spiders.English_corpus_gutenberg import EnglishCorpusGutenbergSpider
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
            image_urls = item["image_urls"]
            for url in image_urls:
                thumb_guid = hashlib.sha1(url.encode('utf8')).hexdigest()
                sql = 'INSERT INTO Img(img_name, url) VALUES(%s,%s)'
                self.db_cur.execute(sql, (thumb_guid, url))

        if isinstance(spider, TranslateBaiduSpider) or isinstance(spider, TranslateYoudaoSpider):
            values = (
                item['category'],
                item['title'],
                item['item_id'],
                item['content'],
            )
            sql = 'INSERT INTO {db_name}(source,word,md,sentence) VALUES(%s,%s,%s,%s)'.format(
                db_name="translate_sentence")  # 将表名设置为参数形式
            self.db_cur.execute(sql, values)
            self.db_conn.commit()
        elif isinstance(spider, EnglishCorpusGutenbergSpider):
            self.insert_db("English_corpus_gutenberg", item)
        return item


class RedisPipeline(object):
    def __init__(self):
        self.db_conn = None
        self.fingerprint_key = 'fingerprint_temp'

    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 6379)
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

    def check_url_crawled(self, url):
        fingerprint = self.generate_fingerprint(url)
        if not self.fingerprint_exist(self.fingerprint_key, fingerprint):
            self.insert_fingerprint(self.fingerprint_key, fingerprint)
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
