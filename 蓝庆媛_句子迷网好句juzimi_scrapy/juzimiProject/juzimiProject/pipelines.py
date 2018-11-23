# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs
class JuzimiprojectPipeline(object):
    def process_item(self, item, spider):
        filePath = "./"+u"句子迷"
        if (not os.path.exists(filePath)):
            os.makedirs(filePath)
        f = codecs.open(filePath+"/"+str(item['id'])+".txt", 'w', encoding="utf-8")  #打开文件
        f.write("country:" + item['country'] + "\r\n")
        f.write("dynasty:" + item['dynasty'] + "\r\n")
        f.write("sentence:" + item['sentence'] + "\r\n")
        f.write("origin:" + item['origin'] + "\r\n")
        f.write("author:" + item['author'] + "\r\n")
        f.write("tag:" + item['tag'] + "\r\n")
        f.close()  # 关闭文件
        return item
