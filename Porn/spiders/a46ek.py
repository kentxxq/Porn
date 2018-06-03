# coding:utf-8


import scrapy
import html5lib
from bs4 import BeautifulSoup
from Porn.items import PornItem
import re
import io
import datetime
import logging
import subprocess
from urllib.parse import quote
import struct
from scrapy.http import Request


class A46ekSpider_10(scrapy.Spider):
    name = 'a46_10'
    # 193.112.129.108是ip地址，发现失效了，可以直接去去拿最新的地址
    # 额。。居然放在。。我什么都不知道。。
    # 后续很有可能会删掉这个页面
    start_urls = ['http://www.46fn.com/list/10.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Porn.pipelines.PornPipeline': 400
        },
        'SPIDER_MIDDLEWARES_BASE': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        }
    }

    table = 'a46'
    ua = 'PC'
    category = '制服丝袜'

    def parse(self, response):
        """
        在入口页面进行解析
        """

        data = response.body
        soup = BeautifulSoup(data, 'html5lib')
        lis = soup.select('.text li')
        baba = response.url
        for li in lis:
            detail_url = li.find('a').get('href')
            # 如果exist_list为空，则全量爬取。否则增量爬取
            if self.exist_list and detail_url in self.exist_list:
                raise scrapy.exceptions.CloseSpider(
                    '截止到'+response.urljoin(detail_url)+'，增量爬取完成' + self.name)
            item = PornItem()
            item['category'] = self.category
            item['name'] = li.find('img').get('alt')
            item['video_intro'] = item['name']
            # 因为部分的路径包括有中文字符，所以做一次处理
            item['img_url'] = quote(li.find('img').get('src'), safe=':/')
            item['update_date'] = li.find(
                'p', text=re.compile('更新日期')).text[-10:]
            item['detail_url'] = response.urljoin(detail_url)
            yield response.follow(detail_url, self.parse_detail, meta={'item': item})

        next_page = soup.find('a', text=re.compile('下一页'))['href']
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        """
        在播放页面进行解析
        """

        page_detail = io.StringIO(response.body.decode('gbk'))
        item = response.meta['item']
        for line in page_detail.readlines():
            if """f:'""" in line:
                # 同样也要处理url
                item['video_url'] = quote(line.strip()[3: - 2], safe=':/')
                yield Request(item['video_url'], self.return_item, meta={'item': item, 'video': '1'})

    def return_item(self, response):
        if response.status in range(200, 301):
            item = response.meta['item']
            item['duration'] = response.body.decode('utf-8')
            yield item
        else:
            print('mp4获取时长失败')


class A46ekSpider_2(A46ekSpider_10):
    name = 'a46_2'
    category = '亚洲日韩'
    start_urls = ['http://www.46fn.com/list/2.html']


class A46ekSpider_8(A46ekSpider_10):
    name = 'a46_8'
    category = '偷拍视频'
    start_urls = ['http://www.46fn.com/list/8.html']
