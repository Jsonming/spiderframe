# ‐*‐ coding: utf‐8 ‐*‐
import requests
from spiderframe.items import SpiderframeItem
from spiderframe.items import ImgsItem

phone = 17749857569

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.duplicates[spider] = set()

    def spider_closed(self, spider):
        del self.duplicates[spider]

    def process_item(self, item, spider):
        if item['category'] in self.duplicates[spider]:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.duplicates[spider].add(item['category'])
        print(item)
        return item


# class Dingding_monitor(object):
#     # def __init__(self, func):
#     #     self.__func = func
#
#     def send_message(self,item):
#         url = "https://oapi.dingtalk.com/robot/send?access_token=21be857aa6e4480caaf0dda29623a9e29ad55b47d3bee9531e8f8705da56b3ee"
#         headers = {'content-type': 'application/json'}
#         if isinstance(item, ImgsItem): #or SpiderframeItem
#             category = item["category"]
#             try:
#                 DuplicatesPipeline()
#                 # resp = func(*args)
#             except Exception as e:
#                 json_content = {'msgtype': "text",
#                                 "text": {"content": "{file_name} 异常报警,报警信息：{msg}".format(file_name=category,
#                                                                                          msg=e.__str__())},
#                                 "at": {
#                                     "atMobiles": [
#                                         phone
#                                     ],
#                                     "isAtAll": False
#                                 }}
#                 raise e
#
#             else:
#                 json_content = {'msgtype': "text",
#                                 "text": {"content": "{file_name} 运行完成".format(file_name=category)},
#                                 "at": {
#                                     "atMobiles": [
#                                         phone
#                                     ],
#                                     "isAtAll": False
#                                 }
#                                 }
#             finally:
#                 flag_resp = requests.post(url=url, headers=headers, json=json_content)
#                 print(flag_resp.text)
#             # return resp
#
#
# Dingding_monitor()


DuplicatesPipeline()

"""
Extension for collecting core stats like items scraped and start/finish times
"""
import datetime

from scrapy import signals

class CoreStats(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(o.response_received, signal=signals.response_received)
        return o

    def spider_opened(self, spider):
        self.stats.set_value('start_time', datetime.datetime.utcnow(), spider=spider)

    def spider_closed(self, spider, reason):
        self.stats.set_value('finish_time', datetime.datetime.utcnow(), spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)

    def item_scraped(self, item, spider):
        self.stats.inc_value('item_scraped_count', spider=spider)

    def response_received(self, spider):
        self.stats.inc_value('response_received_count', spider=spider)

    def item_dropped(self, item, spider, exception):
        reason = exception.__class__.__name__
        self.stats.inc_value('item_dropped_count', spider=spider)
        self.stats.inc_value('item_dropped_reasons_count/%s' % reason, spider=spider)
