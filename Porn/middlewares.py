# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
from scrapy.http import Request
from scrapy.http import Response
# from selenium.webdriver.chrome import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from scrapy.http import TextResponse, HtmlResponse
# from Porn.selenium_class.custom_wait import mp4_element_load_complete
import logging
import struct
from io import StringIO
import scrapy


class PornSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PornDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Ua(UserAgentMiddleware):
    """
    切换User-Agent
    """
    PC_uas = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
              'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
              "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
              "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
              "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
              "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
              "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
              "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
              "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
              "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
              "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]

    Mobile_uas = ['Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
                  'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                  'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                  'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36']

    def process_request(self, request, spider):
        if spider.ua == 'Mobile':
            ua = random.choice(self.Mobile_uas)
            request.headers['User-Agent'] = ua
        if spider.ua == 'PC':
            ua = random.choice(self.PC_uas)
            request.headers['User-Agent'] = ua


# class SeleniumDownloaderMiddleware(object):
#     """
#     selenium下载中间件
#     """

#     def __init__(self, *args, **kwargs):
#         options = webdriver.Options()

#         UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
#         mobileEmulation = {"userAgent": UA}
#         options.add_experimental_option('mobileEmulation', mobileEmulation)
#         options.set_headless(headless=True)
#         self.driver = webdriver.WebDriver(chrome_options=options)
#         print('初始化')

#     @classmethod
#     def from_crawler(cls, crawler):
#         o = cls()
#         crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
#         return o

#     def process_request(self, request, spider):
#         if 'mp' in request.meta:
#             self.driver.get(request.url)
#             try:
#                 wait = WebDriverWait(self.driver, 10)
#                 video_url = wait.until(mp4_element_load_complete())
#                 if video_url:
#                     return HtmlResponse(request.url, body=video_url, encoding="utf-8", request=request)
#             except Exception:
#                 print('出错了')

#         return None

#     def spider_closed(self, spider):
#         self.driver.quit()
#         print('浏览器正常关闭')

class DurationDownloaderMiddle(object):
    def _set_range_headers(self, seek=0):
        headers = {'Range': 'bytes={}-{}'.format(seek, seek + 7)}
        return headers

    def process_request(self, request, spider):
        if 'video' in request.meta and 'seek' not in request.meta:
            item = request.meta['item']
            if '.mp4' in request.url:
                return Request(request.url,
                               headers=self._set_range_headers(0),
                               callback=spider.return_item,
                               #    errback=spider.return_item,
                               meta={'item': item, 'seek': 0, 'video': '1'}, dont_filter=True)
            elif '.m3u8' in request.url:
                Request(request.url,
                        callback=spider.parse_3GPHP,
                        errback=spider.parse_3GPHP,
                        meta={'item': item, 'm3u8': '1'}, dont_filter=True)
        return None

    def process_response(self, request, response, spider):
        # 处理m3u8时长
        if '.m3u8' in request.url:
            i = 0
            data = response.body.decode('utf-8')
            data = StringIO(data)
            for line in data.readlines():
                if line.startswith('#EXTINF:'):
                    i = float(line.replace(',', '').split(':')[1]) + i
            i = str(int(i)).encode('utf-8')
            return Response(response.url, body=i, request=request)

        # 处理mp4时长
        if 'video' in request.meta and 'seek' in request.meta and response.status in range(200, 301):
            item = request.meta['item']
            if 'moov' in request.meta:
                time_scale = int(struct.unpack('>I', response.body[:4])[0])
                duration = int(struct.unpack('>I', response.body[-4:])[0])
                duration = str(int(duration/time_scale)).encode('utf-8')
                return Response(response.url, body=duration, request=request)
            seek = request.meta['seek']
            try:
                size = int(struct.unpack('>I', response.body[:4])[0])
                flag = response.body[-4:].decode('ascii')
            except Exception:
                print(request.url)
                raise scrapy.exceptions.CloseSpider()
            if flag == 'moov':
                return Request(response.url,
                               callback=spider.return_item,
                               errback=spider.return_item,
                               headers=self._set_range_headers(seek+28),
                               meta={'item': item, 'seek': seek+28, 'moov': 1, 'video': 1}, dont_filter=True)
            return Request(response.url,
                           callback=spider.return_item,
                           errback=spider.return_item,
                           headers=self._set_range_headers(size + seek),
                           meta={'item': item, 'seek': seek + size, 'video': '1'}, dont_filter=True)
        return response
