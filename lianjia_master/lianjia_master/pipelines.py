# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

from lianjia_master import settings
from lianjia_master.items import LianjiaMasterItem


class LianjiaMasterPipeline(object):
    def __init__(self):
        """连接redis"""
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def process_item(self, item, spider):
        """将item['url']保存到redis中"""
        if isinstance(item, LianjiaMasterItem):
            self.conn.lpush('lianjia:start_urls', item['url'])
        return item
