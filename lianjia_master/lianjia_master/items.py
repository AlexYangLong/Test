# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# url model类
class LianjiaMasterItem(scrapy.Item):
    url = scrapy.Field()
