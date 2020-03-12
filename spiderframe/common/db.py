#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 18:50
# @Author  : yangmingming
# @Site    : 
# @File    : db.py
# @Software: PyCharm
import redis
import pymysql
from spiderframe import settings
from spiderframe.common.common import md5


class SSDBCon(object):
    def __init__(self):
        """
        初始化连接SSDB数据库,
        链接SSDB数据库没有使用SSDB客户端，使用的是Redis客户端有两个原因
            1.可以无缝对接
            2.框架配合scrapy_redis使用
            3.这里的函数，没有删除数据函数，如果要执行删除操作 到数据库删除  SSDB数据库命令参考
             http://ssdb.io/docs/zh_cn/commands/index.html

        """
        db_host = settings.REDIS_HOST
        db_port = settings.REDIS_PORT
        self.conn = redis.StrictRedis(host=db_host, port=db_port)

    def connection(self):
        """
        返回数据库连接
        :return:
        """
        return self.conn

    def insert_to_list(self, name, value):
        """
        向列表中插入单个的值
        :param name: 列表名称
        :param value: 要插入的值
        :return:
        """
        if isinstance(value, str):
            self.conn.lpush(name, value)
        elif isinstance(value, list) or isinstance(value, tuple):
            self.conn.lpush(name, *value)

    def get_list(self, name, start=0, end=-1):
        """
        获取列表的内容
        :param name:
        :param start: 开始索引
        :param end: 结束索引
        :return:
        """
        return self.conn.lrange(name=name, start=start, end=end)

    def insert_to_hashmap(self, name, key, value=1):
        """
        插入到集合中,由于SSDB 没有set数据类型， 这里的集合采用排序集合sorted set
        :return:
        """
        if isinstance(key, str):
            self.conn.hset(name=name, key=key, value=value)
        else:
            raise TypeError("expected string got {}".format(key))

    def insert_finger(self, name, value):
        """
        将字符串md5插入集合
        :param name:
        :param value:
        :return:
        """
        self.insert_to_hashmap(name, md5(value))

    def exist_finger(self, name, value):
        """
        判断指纹是否存在
        :param name: 指纹库
        :param value: 需要验证的值
        :return:
        """
        return self.exist_in_hashmap(name, md5(value))

    def get_set(self, name, start=0, end=-1):
        """
        获取集合中的元素
        :param name:集合的键
        :return:
        """
        return self.conn.zrange(name=name, start=start, end=end)

    def exist_in_hashmap(self, name, key):
        """
        判断值是否在集合中
        :param name: 集合名称
        :param value: 值
        :return:
        """
        return self.conn.hexists(name=name, key=key)

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.conn.connection_pool.disconnect()


class MysqlCon(object):
    def __init__(self):
        """
        初始化连接mysql数据库
        """
        self.db_conn = pymysql.connect(
            host='123.56.11.156',
            user='sjtUser',
            passwd='sjtUser!1234',
            port=3306,
            db='spiderframe',
            charset='utf8',
            use_unicode=True)
        self.db_cur = self.db_conn.cursor()

    def insert_data(self, table_name, item):
        """
        插入数据到数据中
        :param table_name:
        :param item:
        :return:
        """
        keys, values = [], []
        for key, value in item.items():
            keys.append(key)
            values.append(value)

        para = ["%s"] * len(keys)
        sql = 'INSERT INTO {db_name}({keys}) VALUES({para})'.format(db_name=table_name, keys=",".join(keys),
                                                                    para=",".join(para))
        self.db_cur.execute(sql, values)
        self.db_conn.commit()

    def create_table(self, table_name):
        """
        创建数据库
        :param table_name:
        :return:
        """
        sql = """create table {} (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `spider_name` varchar(32),
              `fingerprint` varchar(32),
              `category` varchar(32),
            
              `url` varchar(480),
              `title` varchar(480),
              `content` longtext,
              PRIMARY KEY (`id`)
            )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;""".format(table_name)
        self.db_cur.execute(sql)
        self.db_conn.commit()

    def exist_table(self, table_name):
        """
        判断表是否存在， 查询表是否存在
        :param table_name:
        :return:
        """
        self.db_cur.execute(
            "select count(1) from information_schema.tables where table_name ='{table_name}';".format(**locals()))
        return self.db_cur.fetchone()[0]

    def close(self):
        self.db_conn.commit()
        self.db_conn.close()
