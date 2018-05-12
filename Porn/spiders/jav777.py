# coding:utf-8

import scrapy
from scrapy import Request
import html5lib
from bs4 import BeautifulSoup
from Porn.items import Jav777Item
from Porn.selenium_class.custom_wait import mp4_element_load_complete as mp4


class Jav777Spider(scrapy.Spider):
    name = 'jav777'
    allowed_domains = ['jav777.cc']
    start_urls = ['http://www.jav777.cc/page/1']
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'Porn.pipelines.A46ekPipeline': 400
        },
        'DOWNLOADER_MIDDLEWARES': {
            'Porn.middlewares.SeleniumDownloaderMiddleware': 800
        },
        'SPIDER_MIDDLEWARES_BASE': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        }
    }

    ua = 'Mobile'

    # google翻译的。。不知道什么意思
    category = '家'

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html5lib')
        containers = soup.select('.post-container .post')
        for container in containers:
            item = Jav777Item()
            item['name'] = container.find('a').text
            item['img_url'] = container.find('img').get('src')
            item['detail_url'] = container.find('a').get('href')
            # yield response.follow(item['detail_url'], self.parse_detail, meta={'mp': 123})
            yield response.follow(item['detail_url'], self.parse_detail, meta={'item': item})
            # raise scrapy.exceptions.CloseSpider('跑一个关了')

    def parse_detail(self, response):
        data = response.body
        item = response.meta['item']
        soup = BeautifulSoup(data, 'html5lib')
        url = soup.find(id='allmyplayer').get('src')
        # print('开始爬取'+url)
        yield response.follow(url, self.parse_iframe, meta={'mp': 1, 'item': item})

    def parse_iframe(self, response):
        # print('进入iframe处理!!!!')
        item = response.meta['item']
        item['video_url'] = response.body.decode('utf-8')
        print(item)
        yield item
