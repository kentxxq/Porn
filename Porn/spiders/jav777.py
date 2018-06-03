# coding:utf-8

import scrapy
from scrapy import Request
import html5lib
from bs4 import BeautifulSoup
from Porn.items import PornItem
# from Porn.selenium_class.custom_wait import mp4_element_load_complete as mp4
from Porn.tools.mediainfo import *
import html
import re
from urllib.parse import unquote


class Jav777Spider(scrapy.Spider):
    name = 'jav777'
    allowed_domains = ['jav777.cc']
    start_urls = ['http://www.jav777.cc/page/1']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Porn.pipelines.PornPipeline': 400
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'Porn.middlewares.SeleniumDownloaderMiddleware': 800
        # },
        'SPIDER_MIDDLEWARES_BASE': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        }
    }
    handle_httpstatus_list = [404, 301]

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
            detail_url = item['detail_url']
            # 如果exist_list为空，则全量爬取。否则增量爬取
            if self.exist_list and detail_url in self.exist_list:
                raise scrapy.exceptions.CloseSpider(
                    '截止到' + response.urljoin(detail_url) + '，增量爬取完成' + self.name)
            if detail_url == 'http://www.jav777.cc/atid-292-%e5%bc%b7%e8%a5%b2%e4%bd%8f%e6%89%80%e5%bc%b7%e5%a7%a6%e8%a8%98%e9%8c%84-%e4%bd%90%e4%bd%90%e6%9c%a8%e6%98%8e%e5%b8%8c%e4%b8%ad%e6%96%87%e5%ad%97%e5%b9%95.html':
                yield response.follow(item['detail_url'], self.parse_detail, meta={'item': item})
        # next_page = soup.find(class_='post-nav-older').get('href')
        # yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        data = response.body
        item = response.meta['item']
        soup = BeautifulSoup(data, 'html5lib')
        item['update_date'] = soup.find(class_='post-date').text
        item['category'] = self.category
        item['video_intro'] = soup.find(class_='post-content').find('p').text
        url = soup.find(id='allmyplayer').get('src')
        yield response.follow(url, self.parse_iframe, meta={'item': item})

    def parse_iframe(self, response):
        item = response.meta['item']
        data = response.body
        text = BeautifulSoup(data, 'html5lib').text
        p = re.search('get3G.php\?.*&mp4=', text).span()
        url = text[p[0]:p[1]]
        url = re.sub('rand=[0-9]*&', '', url).strip()
        item['tmp'] = response.urljoin(url)
        url = url + '1'
        yield response.follow(url, self.parse_3GPHP, meta={'item': item})

    def parse_3GPHP(self, response):
        item = response.meta['item']
        data = response.body
        text = BeautifulSoup(data, 'html5lib').text
        text = unquote(text)
        if 'm3u8' not in response.meta:
            p = re.search('src=\\\\\"http:\/\/.*\?sk=.*se=\d+', text).span()
        else:
            p = re.search('src=\\\\\"http:\/\/.*\?', text).span()
        video_url = text[p[0]:p[1]].strip().split('"')[1][0:-1]
        item['video_url'] = video_url
        print(video_url)
        yield Request(item['video_url'], self.return_item,
                      meta={'video': '1', 'item': item}, dont_filter=True)

    def return_item(self, response):
        print(response.meta)
        item = response.meta['item']
        if response.status not in range(200, 301) and '.mp4' in response.url:
            print('mp4获取失败:', response.status)
            # mp4失败后获取m3u8
            url = item['tmp']+'0'
            yield Request(url, self.parse_3GPHP, meta={'item': item, 'video': '1', 'm3u8': '1'})
        elif response.status in range(200, 301) and 'm3u8' in response.url:
            item['duration'] = response.body.decode('utf-8')
            yield item
        else:
            print('获取失败')
