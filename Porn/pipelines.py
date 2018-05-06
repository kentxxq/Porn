# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging
import scrapy


class A46ekPipeline(object):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(host=settings['A46EK_IP'],
                   port=settings['A46EK_PORT'],
                   username=settings['A46EK_USERNAME'],
                   password=settings['A46EK_PASSWORD'])

    def process_item(self, item, spider):
        try:
            self.a46ek.insert_one(dict(item))
        except DuplicateKeyError:
            self.a46ek.save(dict(item))
        except Exception as e:
            raise scrapy.exceptions.CloseSpider('数据处理出现错误！'+e)
        finally:
            return item

    def open_spider(self, spider):
        self.a46ek = MongoClient(host=self.host,
                                 port=self.port,
                                 username=self.username,
                                 password=self.password)['porn']['a46ek']
        spider.exist_list = []
        if hasattr(spider, 'incremental'):
            if spider.incremental == True:
                results = self.a46ek.find()
                for result in results:
                    spider.exist_list.append(result['detail_url'])

    def close_spider(self, spider):
        pass
