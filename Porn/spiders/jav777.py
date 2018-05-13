# coding:utf-8

import scrapy
from scrapy import Request
import html5lib
from bs4 import BeautifulSoup
from Porn.items import PornItem
from Porn.selenium_class.custom_wait import mp4_element_load_complete as mp4
from Porn.tools.mediainfo import Mp4info


class Jav777Spider(scrapy.Spider):
    name = 'jav777'
    allowed_domains = ['jav777.cc']
    start_urls = ['http://www.jav777.cc/page/1']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Porn.pipelines.PornPipeline': 400
        },
        'DOWNLOADER_MIDDLEWARES': {
            'Porn.middlewares.SeleniumDownloaderMiddleware': 800
        },
        'SPIDER_MIDDLEWARES_BASE': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        }
    }
    table = 'jav777'

    ua = 'Mobile'

    # google翻译的。。不知道什么意思
    category = '家'

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html5lib')
        containers = soup.select('.post-container .post')
        for container in containers:
            item = PornItem()
            item['name'] = container.find('a').text
            item['img_url'] = container.find('img').get('src')
            item['detail_url'] = container.find('a').get('href')
            yield response.follow(item['detail_url'], self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        data = response.body
        item = response.meta['item']
        soup = BeautifulSoup(data, 'html5lib')
        item['update_date'] = soup.find(id='post-date').text
        item['category'] = self.category
        item['video_intro'] = soup.find(class_='post-content').find('p').text
        url = soup.find(id='allmyplayer').get('src')
        yield response.follow(url, self.parse_iframe, meta={'mp': 1, 'item': item})

    def parse_iframe(self, response):
        item = response.meta['item']
        item['video_url'] = response.body.decode('utf-8')
        item['duration'] = Mp4info(item['video_url']).get_duration()
        yield item
