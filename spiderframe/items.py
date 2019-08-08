# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderframeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    ori_url = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()

    item_id = scrapy.Field()
    item_name = scrapy.Field()
    item_time_long = scrapy.Field()
    item_time_unit = scrapy.Field()


class ImgsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    category = scrapy.Field()
    image_urls = scrapy.Field()     # 这个图片的URL 类型:list
    images = scrapy.Field()         # 这个看源码是结果字段，也不知道要它干啥， 有个屌用！
