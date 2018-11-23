# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JuzimiprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = scrapy.Field()#国家
    dynasty = scrapy.Field()#朝代
    sentence = scrapy.Field()#句子
    origin = scrapy.Field()#出处
    author = scrapy.Field()#作者
    tag = scrapy.Field()#标签
    id = scrapy.Field()#文件名
