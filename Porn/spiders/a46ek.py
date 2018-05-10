# coding:utf-8


import scrapy
import html5lib
from bs4 import BeautifulSoup
from Porn.items import A46ekItem
import re
import io
import datetime
import logging
import subprocess
from urllib.parse import quote
from Porn.tools.mediainfo import Mp4info


class A46ekSpider_10(scrapy.Spider):
    name = 'a46ek_10'
    allowed_domains = ['46ek.com']
    start_urls = ['http://www.46ek.com/list/10.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Porn.pipelines.A46ekPipeline': 400
        }
    }

    ua = 'PC'

    category = '制服丝袜'

    def parse(self, response):
        """
        在入口页面进行解析
        """

        data = response.body
        soup = BeautifulSoup(data, 'html5lib')
        lis = soup.select('.text li')
        for li in lis:
            detail_url = li.find('a').get('href')
            # 如果exist_list为空，则全量爬取。否则增量爬取
            if self.exist_list and detail_url in self.exist_list:
                raise scrapy.exceptions.CloseSpider(
                    '截止到'+response.urljoin(detail_url)+'，增量爬取完成' + self.name)
            item = A46ekItem()
            item['category'] = self.category
            item['name'] = li.find('img').get('alt')
            # 因为部分的路径包括有中文字符，所以做一次处理
            item['img_url'] = quote(li.find('img').get('src'), safe=':/')
            item['update_date'] = li.find(
                'p', text=re.compile('更新日期')).text[-10:]
            item['detail_url'] = response.urljoin(detail_url)
            yield response.follow(detail_url, self.parse_detail, meta={'item': item})

        next_page = soup.find('a', text=re.compile('下一页')).get('href')
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
                # 由于部分网站是有视频长度信息可以爬取的，所以统一把时长信息写到spider里
                mp4file = Mp4info(item['video_url'])
                item['duration'] = mp4file.get_duration()
                yield item


class A46ekSpider_2(A46ekSpider_10):
    name = 'a46ek_2'
    category = '亚洲日韩'
    start_urls = ['http://www.46ek.com/list/2.html']


class A46ekSpider_8(A46ekSpider_10):
    name = 'a46ek_8'
    category = '偷拍视频'
    start_urls = ['http://www.46ek.com/list/8.html']
