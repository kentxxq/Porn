# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


"""
本来打算用redis，但是用name做key，分类就只能放到list里面去了。很麻烦
就选用了mongodb来存放数据

把同一个网站上面的不同入口分开处理，这样就可以简单实现增量爬取
"""
