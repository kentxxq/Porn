# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class A46ekItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail_url = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    update_date = scrapy.Field()
    video_url = scrapy.Field()
    category = scrapy.Field()
    duration = scrapy.Field()
