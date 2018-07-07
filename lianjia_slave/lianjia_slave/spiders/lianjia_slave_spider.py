from scrapy import Selector
from scrapy_redis.spiders import RedisSpider

from lianjia_slave.items import LianjiaESFItem, LianjiaXFItem, LianjiaCZFItem


class LianjiaSlaveSpider(RedisSpider):
    # 爬虫名 唯一
    name = 'lianjia_slave'

    # redis中url的键
    redis_key = 'lianjia:start_urls'

    def parse(self, response):
        """
        解析爬虫返回的response
        :param response:
        :return:
        """
        html = Selector(response)

        # 因为Master爬虫把二手房、新房、出租房所有的url都储存在一个键对应的列表中
        # 所以要判断返回的response属于哪一个页面，在进行解析
        esf = html.xpath('/html/body/div[4]/div[1]/div[2]/h2/text()').extract()
        xf = html.xpath('/html/body/div[4]/div[2]/span/text()').extract()
        czf = html.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/h2/text()').extract()

        # 进行判断
        if esf:  # 二手房
            lis = html.xpath('/html/body/div[4]/div[1]/ul/li[@class="clear"]')
            for li in lis:
                item = LianjiaESFItem()
                item['house_code'] = li.xpath('./a/@data-housecode').extract()[0]
                item['house_link'] = li.xpath('./div/div/a/@href').extract()[0]
                item['house_origin'] = '链家'
                item['img_src'] = li.xpath('./a/img/@src').extract()[0]
                item['title'] = li.xpath('./div/div/a/text()').extract()[0]
                item['total_price'] = li.xpath('./div[1]/div[6]/div[1]/span/text()').extract()[0] + li.xpath('./div[1]/div[6]/div[1]/text()').extract()[0]
                item['unit_price'] = li.xpath('./div[1]/div[6]/div[2]/span/text()').extract()[0]
                item['address'] = li.xpath('./div/div[2]/div/a/text()').extract()[0]
                item['info'] = self.split_str(li.xpath('./div/div[2]/div/text()').extract()[0])
                item['floor'] = li.xpath('./div[1]/div[3]/div/text()').extract()[0] + li.xpath('./div[1]/div[3]/div/a/text()').extract()[0]
                item['tag'] = li.xpath('.//div[@class="tag"]/span/text()').extract()
                item['type'] = 'ershoufang'
                item['city'] = '成都'
                item['area'] = li.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[1]/a[@class="selected"]/text()').extract()[0]
                yield item
        elif xf:  # 新房
            lis = html.xpath('//ul[@class="resblock-list-wrapper"]/li[@class="resblock-list"]')
            for li in lis:
                item = LianjiaXFItem()
                item['house_code'] = li.xpath('./@data-project-name').extract()[0]
                item['house_link'] = 'https://cd.fang.lianjia.com' + li.xpath('./a/@href').extract()[0]
                item['house_origin'] = '链家'
                item['img_src'] = li.xpath('./a/img/@src').extract()[0]
                item['title'] = li.xpath('./div/div[1]/a/text()').extract()[0]
                item['tag'] = li.xpath('./div/div[1]/span/text()').extract()
                item['area'] = li.xpath('./div/div[2]/span[1]/text()').extract()[0]
                total_price = li.xpath('./div/div[6]/div[2]/text()').extract()
                if total_price:
                    item['total_price'] = total_price[0]
                else:
                    item['total_price'] = ''
                item['unit_price'] = ''.join(li.xpath('./div/div[6]/div/span/text()').extract())

                item['address'] = li.xpath('./div/div[2]/span[2]/text()').extract()[0] + '-' + li.xpath('./div/div[2]/a/text()').extract()[0]
                construction_area = li.xpath('./div/div[3]/span/text()').extract()
                if construction_area:
                    item['construction_area'] = construction_area[0]
                else:
                    item['construction_area'] = ''

                house_consultant = li.xpath('./div/div[4]/span/text()').extract()
                if house_consultant:
                    item['house_consultant'] = house_consultant[0]
                else:
                    item['house_consultant'] = ''

                item['type'] = 'xinfang'
                item['city'] = '成都'
                yield item
        elif czf:  # 出租房
            lis = html.xpath('//*[@id="house-lst"]/li')
            for li in lis:
                item = LianjiaCZFItem()
                item['house_code'] = li.xpath('./@data-id').extract()[0]
                item['house_link'] = li.xpath('./div[1]/a/@href').extract()[0]
                item['house_origin'] = '链家'
                item['img_src'] = li.xpath('./div[1]/a/img/@src').extract()[0]
                item['title'] = li.xpath('./div[2]/h2/a/text()').extract()[0]

                item['village'] = li.xpath('./div[2]/div[1]/div[1]/a/span/text()').extract()[0].strip()
                guige = li.xpath('./div[2]/div[1]/div[1]/span[1]/span/text()').extract()[0].strip()
                mj = li.xpath('./div[2]/div[1]/div[1]/span[2]/text()').extract()[0].strip()
                cx = li.xpath('./div[2]/div[1]/div[1]/span[3]/text()').extract()[0].strip()
                item['info'] = [guige, mj, cx]

                item['floor'] = li.xpath('./div[2]/div[1]/div[2]/div/text()').extract()[0]
                if len(li.xpath('./div[2]/div[1]/div[2]/div/text()').extract()) > 1:
                    item['yrb'] = li.xpath('./div[2]/div[1]/div[2]/div/text()').extract()[1]
                else:
                    item['yrb'] = ''

                tag1 = li.xpath('./div[2]/div[1]/div[3]/div/div/span[@class="fang-subway-ex"]/span/text()').extract()
                tag2 = li.xpath('./div[2]/div[1]/div[3]/div/div/span[@class="haskey-ex"]/span/text()').extract()
                tag3 = li.xpath('./div[2]/div[1]/div[3]/div/div/span[@class="decoration-ex"]/span/text()').extract()
                tag = []
                if tag1:
                    tag.append(tag1[0])
                if tag2:
                    tag.append(tag2[0])
                if tag3:
                    tag.append(tag3[0])
                item['tag'] = tag

                item['type'] = 'chuzufang'
                item['city'] = '成都'
                item['area'] = html.xpath('//*[@id="filter-options"]/dl[1]/dd/div[1]/a[@class="on"]/text()').extract()[0]
                item['update_time'] = li.xpath('./div[2]/div[2]/div[2]/text()').extract()[0]
                item['price'] = li.xpath('./div[2]/div[2]/div[1]/span/text()').extract()[0] + li.xpath('./div[2]/div[2]/div[1]/text()').extract()[0]
                yield item

    def split_str(self, origin_str):
        """
        将源字符串根据 '|' 拆分，并去除拆分后每个子串左右两边的空格
        :param origin_str:
        :return:
        """
        return [s.strip() for s in origin_str.split('|')[1:]]
