# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
from juzimiProject.items import JuzimiprojectItem
class JuzimispiderSpider(scrapy.Spider):
    name = 'juzimispider'
    allowed_domains = ['juzimi.com']
    start_urls = ['https://www.juzimi.com/writers']
    website = "https://www.juzimi.com"
    id=1

    def parse(self, response):
        soup=bs(response.body, "lxml")
        aChinaList = soup.find(attrs={'class':'wrlist'}).findAll('a')# 中国各朝代链接
        aFroginList = soup.findAll(attrs={'class':'wrlist'})[1].findAll('a') # 外国链接
        j = 1
        for a in aChinaList + aFroginList:  # 两个列表相加，遍历各个链接
            item = JuzimiprojectItem()
            if j <= len(aChinaList):  # 中国各朝代
                item['country'] = '中国'  # ***国家名***
                item['dynasty'] = a.get_text().strip()  # ***取得朝代***
                url = self.website + a.get('href')  # 例：https://www.juzimi.com/dynasty/先秦
            else: # 外国
                item['country'] = a.get_text().strip()  # ***国家名***
                item['dynasty'] = ''  # ***外国无朝代***
                url = self.website + a.get('href')  # 例：https://www.juzimi.com/country/美国
            j += 1
            yield scrapy.Request(url=url, meta={'meta_1': item}, callback=self.second_parse,dont_filter=True)

    def second_parse(self, response):
        meta1 = response.meta['meta_1']
        soup2 = bs(response.body, "lxml")
        aLinks = soup2.select('.views-field-name a[href]')#取得该页中所有的作者名字的链接
        for a in aLinks:
            item = JuzimiprojectItem()
            item['country']=meta1['country']
            item['dynasty']=meta1['dynasty']
            item['author'] = a.text.strip()  # ***取作者名字***
            url = self.website + a.get('href')  # 例：https://www.juzimi.com/writer/庄子
            print(url)
            yield scrapy.Request(url=url, meta={'meta_2': item}, callback=self.parse_detail,dont_filter=True)
        nextPage = soup2.find('.pager-next')
        if nextPage is not None:#取下一页连接
            url = self.website + nextPage.a.get('href')
            print(url)
            yield scrapy.Request(url=url, meta={'meta_1': meta1}, callback=self.second_parse,dont_filter=True)

    def parse_detail(self, response):# 解析具体页面，取出每页的每个句子文本，出处，标签等信息
        meta2 = response.meta['meta_2']
        soup3 = bs(response.body, "lxml")
        try:
            tag = soup3.select('.xqorigcatediv')[0].get_text(",", strip=True).replace('标签：,','').replace('#','')  #*** 标签***# 去除文本内容前后的空白,替换多余字符
        except Exception as e:
            tag = ""
        divList = soup3.select('.views-field-phpcode')  # 装着句子和出处的div标签列表
        for div in divList:
            item = JuzimiprojectItem()
            item['country']=meta2['country']
            item['dynasty']=meta2['dynasty']
            item['author']=meta2['author']
            item['tag']=tag
            try:
                item['sentence'] = div.select('a.xlistju')[0].get_text().strip()  # ***取句子文本***
            except:
                item['sentence']=""
            try:
                item['origin'] = div.select('a.active')[0].get_text().strip()  # ***句子的出处。
            except Exception as e:
                item['origin'] = ""
            item['id']=self.id
            if item['sentence']!="":
                self.id+=1
                yield item
        nextPage = soup3.find('.pager-next')
        if nextPage is not None:  # 取下一页连接
            url = self.website + nextPage.a.get('href')
            yield scrapy.Request(url=url, meta={'meta_2': meta2}, callback=self.parse_detail, dont_filter=True)

