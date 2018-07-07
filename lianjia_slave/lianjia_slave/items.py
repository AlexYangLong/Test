# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 二手房的model类
class LianjiaESFItem(scrapy.Item):
    # 数据保存到MongoDB的文档名
    collection = 'ershoufang'

    # 房屋编码: str
    house_code = scrapy.Field()
    # 房屋url: str
    house_link = scrapy.Field()
    # 房屋来源: str
    house_origin = scrapy.Field()
    # 房屋图片url: str
    img_src = scrapy.Field()
    # 房屋标题: str
    title = scrapy.Field()
    # 房屋总价: str
    total_price = scrapy.Field()
    # 房屋每平米价格: str
    unit_price = scrapy.Field()
    # 房屋地址: str
    address = scrapy.Field()
    # 房屋信息: list
    info = scrapy.Field()
    # 房屋楼层: str
    floor = scrapy.Field()
    # 房屋标签:list
    tag = scrapy.Field()
    # 房屋类型: str：ershoufang、xinfang、chuzufang
    type = scrapy.Field()
    # 所在城市: str
    city = scrapy.Field()
    # 所在区域: str
    area = scrapy.Field()
    # 爬取时间: str
    create_time = scrapy.Field()


# 新房的model类
class LianjiaXFItem(scrapy.Item):
    # 数据保存到MongoDB的文档名
    collection = 'xinfang'

    # 房屋编码: str
    house_code = scrapy.Field()
    # 房屋url: str
    house_link = scrapy.Field()
    # 房屋来源: str
    house_origin = scrapy.Field()
    # 房屋图片url: str
    img_src = scrapy.Field()
    # 房屋标题: str
    title = scrapy.Field()
    # 房屋标签: list
    tag = scrapy.Field()
    # 房屋类型：str: ershoufang、xinfang、chuzufang
    type = scrapy.Field()
    # 所在城市: str
    city = scrapy.Field()
    # 所在区域: str
    area = scrapy.Field()
    # 房屋总价: str
    total_price = scrapy.Field()
    # 房屋每平米价格: str
    unit_price = scrapy.Field()
    # 房屋地址: str
    address = scrapy.Field()
    # 建造面积: str
    construction_area = scrapy.Field()
    # 新房顾问: str
    house_consultant = scrapy.Field()
    # 爬取时间: str
    create_time = scrapy.Field()


# 出租房的model类
class LianjiaCZFItem(scrapy.Item):
    # 数据保存到MongoDB的文档名
    collection = 'chuzufang'

    # 房屋编码: str
    house_code = scrapy.Field()
    # 房屋url: str
    house_link = scrapy.Field()
    # 房屋来源: str
    house_origin = scrapy.Field()
    # 房屋图片url: str
    img_src = scrapy.Field()
    # 房屋标题: str
    title = scrapy.Field()
    # 房屋价格: str
    price = scrapy.Field()
    # 小区名: str
    village = scrapy.Field()
    # 房屋信息: list
    info = scrapy.Field()
    # 房屋楼层: str
    floor = scrapy.Field()
    # 建造年份: str
    yrb = scrapy.Field()
    # 房屋标签: list
    tag = scrapy.Field()
    # 房屋类型: str：ershoufang、xinfang、chuzufang
    type = scrapy.Field()
    # 所在城市: str
    city = scrapy.Field()
    # 所在区域: str
    area = scrapy.Field()
    # 更新时间: str
    update_time = scrapy.Field()
    # 爬取时间: str
    create_time = scrapy.Field()
