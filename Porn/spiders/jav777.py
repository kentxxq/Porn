# coding:utf-8

import scrapy
import html5lib
from bs4 import BeautifulSoup
from Porn.items import Jav777Item
from scrapy_splash import SplashRequest


class Jav777Spider(scrapy.Spider):
    name = 'jav777'
    allowed_domains = ['jav777.cc']
    start_urls = ['http://www.jav777.cc/page/1']
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'ITEM_PIPELINES': {
            # 'Porn.pipelines.A46ekPipeline': 400
        },
        # 因为要去到别的网页抓取，所以把这个限制给去掉
        'SPIDER_MIDDLEWARES_BASE': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        },
        # 下面这两个是按照官网添加的
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        }
    }

    ua = 'Mobile'

    # google翻译的。。不知道什么意思
    category = '家'

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html5lib')
        containers = soup.select('.post-container .post')
        for container in containers:
            item = Jav777Item()
            item['name'] = container.find('a').text
            item['img_url'] = container.find('img').get('src')
            item['detail_url'] = container.find('a').get('href')
            # print(item)
            yield SplashRequest(
                item['detail_url'],
                self.parse_detail,
                args={'wait': 5},
                meta={'item': item},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
                }
            )

    def parse_detail(self, response):
        # print('解析detail'+response.url)
        data = response.body
        # print(data.decode('utf-8'))
        item = response.meta['item']
        # print(data.decode('utf-8'))
        soup = BeautifulSoup(data, 'html5lib')
        # iframe = soup.find(id='allmyplayer').get('src')
        source = soup.find('iframe', attrs={'name': 'allmyplayer'}).get('src')
        print('获取了source:'+source)
        # print(response.urljoin(iframe))
        # yield item

        yield SplashRequest(source, self.parse_iframe, meta={'item': item},
                            args={'wait': 20},
                            headers={
                                # 'Referer': 'http://video.520cc.cc/player777G.php?id=777ccGDTEJrYUNJT1oxTkNoT3NrWGNMcnp3UjczTWJvUUxzdzUrd3h2TEViY1ZMYXZEcEZWRmJnOVpRPT0=',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
        })
        # yield SplashRequest('http://httpbin.org/headers',
        #                     self.parse_iframe, args={'wait': 2},
        #                     headers={
        #                         'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
        #                     })

    def parse_iframe(self, response):
        data = response.body
        soup = BeautifulSoup(data, 'html5lib')
        print('地址啊！！！' + soup.find('source').get('src'))
        # print(data.decode('utf-8'))
