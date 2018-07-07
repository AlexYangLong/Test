import json
import re

import scrapy
from scrapy import Request, Selector

from lianjia_master.items import LianjiaMasterItem


class LianjiaMasterSpider(scrapy.Spider):
    # 爬虫名 唯一
    name = 'lianjia_master'

    base_url = 'https://cd.lianjia.com'
    # 二手房url
    start_ershoufang_url = 'https://cd.lianjia.com/ershoufang'
    # 新房url
    start_xinfang_url = 'https://cd.fang.lianjia.com/loupan/'
    # 租房url
    start_zufang_url = 'https://cd.lianjia.com/zufang/'

    def start_requests(self):
        """
        开始爬取
        :return:
        """
        yield Request(url=self.start_ershoufang_url, callback=self.parse_ershoufang)
        yield Request(url=self.start_xinfang_url, callback=self.parse_xinfang)
        yield Request(url=self.start_zufang_url, callback=self.parse_zufang)

    def parse_ershoufang(self, response):
        """
        根据response解析出二手房页面所有的区域的url，在向下爬取
        :param response:
        :return:
        """
        html = Selector(response)
        area_hrefs = html.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        area_names = html.xpath('//div[@data-role="ershoufang"]/div/a/text()').extract()

        for i in range(len(area_hrefs)):
            # print(area_names[i], area_hrefs[i])
            yield Request(url=self.base_url + area_hrefs[i],
                          callback=self.parse_esf_list_url,
                          meta={'area_href': area_hrefs[i]})

    def parse_esf_list_url(self, response):
        """
        根据response解析出二手房页面每个区域所对应的所有页码的url，并返回给pipeline
        :param response:
        :return:
        """
        html = Selector(response)
        max_page_box = html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        max_page_num = json.loads(max_page_box[0]).get('totalPage')

        for i in range(1, int(max_page_num) + 1):
            item = LianjiaMasterItem()
            item['url'] = self.base_url + response.meta.get('area_href') + 'pg' + str(i)
            yield item

    def parse_xinfang(self, response):
        """
        根据response解析出新房页面所有的区域的url，在向下爬取
        :param response:
        :return:
        """
        html = Selector(response)
        area_hrefs = html.xpath('/html/body/div[2]/div[2]/ul/li/@data-district-spell').extract()
        area_names = html.xpath('/html/body/div[2]/div[2]/ul/li/text()').extract()

        for i in range(len(area_hrefs)):
            # print(area_names[i], area_hrefs[i])
            yield Request(url=self.start_xinfang_url + area_hrefs[i],
                          callback=self.parse_xf_list,
                          meta={'area_href': area_hrefs[i]})

    def parse_xf_list(self, response):
        """
        根据response解析出新房页面每个区域所对应的所有页码的url，并返回给pipeline
        :param response:
        :return:
        """
        html = Selector(response)
        max_page_box = html.xpath('//div[@class="page-box"]/@data-total-count').extract()
        max_page_num = int(max_page_box[0]) // 10 + 1

        for i in range(1, max_page_num + 1):
            item = LianjiaMasterItem()
            item['url'] = self.start_xinfang_url + response.meta.get('area_href') + '/pg' + str(i)
            yield item

    def parse_zufang(self, response):
        """
        根据response解析出出租房页面所有的区域的url，在向下爬取
        :param response:
        :return:
        """
        html = Selector(response)
        area_hrefs = html.xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/@href').extract()
        area_names = html.xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/text()').extract()

        for i in range(1, len(area_hrefs)):
            # print(area_names[i], area_hrefs[i])
            yield Request(url=self.base_url + area_hrefs[i],
                          callback=self.parse_zf_list,
                          meta={'area_href': area_hrefs[i]})

    def parse_zf_list(self, response):
        """
        根据response解析出出租房页面每个区域所对应的所有页码的url，并返回给pipeline
        :param response:
        :return:
        """
        html = Selector(response)
        max_page_box = html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        max_page_num = json.loads(max_page_box[0]).get('totalPage')

        for i in range(1, int(max_page_num) + 1):
            item = LianjiaMasterItem()
            item['url'] = self.base_url + response.meta.get('area_href') + 'pg' + str(i)
            yield item
