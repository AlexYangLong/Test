# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo

from lianjia_slave import settings
from lianjia_slave.items import LianjiaESFItem, LianjiaXFItem, LianjiaCZFItem


class LianjiaSlaveCreateTimePipeline(object):
    """用于给item添加爬取时间"""
    def process_item(self, item, spider):
        item['create_time'] = datetime.now().strftime('%Y-%m-%d %X')
        return item


class LianjiaSlavePipeline(object):
    def __init__(self):
        """连接MongoDB"""
        conn = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        self.db = conn[settings.MONGODB_DB]

    def process_item(self, item, spider):
        """将item数据存储到MongoDB中"""
        if isinstance(item, LianjiaESFItem):
            self.db['ershoufang'].update({'house_code': item['house_code']}, {'$set': item}, True)
        elif isinstance(item, LianjiaXFItem):
            self.db['xinfang'].update({'house_code': item['house_code']}, {'$set': item}, True)
        elif isinstance(item, LianjiaCZFItem):
            self.db['chuzufang'].update({'house_code': item['house_code']}, {'$set': item}, True)
        return item
