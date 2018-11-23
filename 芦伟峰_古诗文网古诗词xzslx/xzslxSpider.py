# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 10:52:15 2018

@author: 卢超人
"""

import requests
import random
import time
import os
from bs4 import BeautifulSoup
ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.5 Safari/537.36"
]
def spyder(url):                         #请求的核心代码
    user_agent = random.choice(ua_list)  # 在User-Agent列表里面，随机选择一个User-Agent
    headers = {'User-Agent': user_agent}
    req=requests.get(url,headers=headers)
    req.encoding='utf-8'                 #使用utf-8解码
    bs=BeautifulSoup(req.content,'lxml')
    return bs

def gushi(url,a,num):                      #筛选内容并写入txt文件，有find方法和select方法
    bs=spyder(url)
    try:                                           #异常处理
        title=bs.select('body div h2')[0].text    #通过DOM树结构查找
        dynasty=bs.select('.f-l a')[1].text        #通过css选择器查找
        author=bs.select('.f-l a')[0].text
        tag=bs.find('div',attrs={'class':'f-l ziliao12'}).text
        content=bs.select('dd,.conview conview_main show')[0].text
    except Exception as e:
        print(e)
    if num=='/0/0/16/0/0/':                    #判断古诗的type类型
        t='诗'
    elif num=='/0/0/13/0/0/':
        t='词'
    elif num=='/0/0/14/0/0/':
        t='曲'
    elif num=='/0/0/17/0/0/':
        t='文言文'
    elif num=='/0/0/12/0/0/':
        t='辞赋'
    if not os.path.exists('gushi\\'):  # 如果文件夹gushi不存在则创建
        os.makedirs('gushi\\')
    with open('gushi\\'+a[5:]+'.txt','w',encoding='utf-8') as f:     #写入txt文件，采用相对路径
        f.write('title：'+title+'\n')
        f.write('dynasty：'+dynasty+'\n')
        f.write('auther：'+author+'\n')
        f.write('tag：'+tag.replace('\n','')+'\n')
        f.write('type：' + t+'\n')
        f.write('content：'+content+'\n')
    print('成功写入'+a)                       #成功写入一个txt文件则告知

def main_py(num,page):                       #从type网页入手，在type网页找到古诗链接并循环访问
    try:                                      #异常处理
        for i in range(1,page+1):
            url='https://www.xzslx.net/gushi'+num+str(i)+'/'       #type网页，其中i为页数
            bs=spyder(url)
            for strong in bs.find_all('strong'):                #在type网页中找到古诗链接
                for a in strong.find_all('a'):
                    a=a['href']
                    url='https://www.xzslx.net'+a
                    gushi(url,a,num)
        time.sleep(5)                       #每爬玩一页睡5秒，反爬
    except Exception as e:
        print(e)

"""
由于type类别在古诗那一页不能直接找到，因此要从首页出发，从type的分类出发，从type网页中找古诗链接来确定古诗的type类型。
'num=/0/0/16/0/0/  page=616'   #诗
'num=/0/0/13/0/0/   page=38'   #词
'num=/0/0/14/0/0/    page=3'   #曲
'num=/0/0/17/0/0/   page=25'   #文言文
'num=/0/0/12/0/0/ page=4851'   #辞赋
"""
main_py('/0/0/16/0/0/',616)      #执行命令
main_py('/0/0/13/0/0/',38)
main_py('/0/0/14/0/0/',3)
main_py('/0/0/17/0/0/',25)
main_py('/0/0/12/0/0/',4851)
print('全部成功写入')
