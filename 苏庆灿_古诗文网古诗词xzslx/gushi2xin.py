# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:14:54 2018

@author: 繁华过后就
"""

import requests,os,re
from bs4 import BeautifulSoup
from urllib.request import urljoin

links=[]

def  create():
    file=os.path.exists("E:\\gushiwen")
    if not file:
        os.makedirs("E:\\gushiwen")
    else:
        print("该文件夹已存在")
    
def download(url,user_agent='wswp',num=2,proxies=None):
    print('Download:',url)
    headers={'User_agent':user_agent}
    try:
        re=requests.get(url,headers=headers,proxies=proxies)
        html=re.text
        if re.status_code>=400:
            print('Error',re.text)
            html=None
            if num and 500<=re.status_code<600:
                return download(url,num-1)
    except requests.exceptions.RequestException as e:
        print('Error',e.reason)
        html=None
    return html    
def get_links(html):
    webpage_regex=re.compile("""<a[^>]+href=["'](.*?)["']""",re.IGNORECASE)
    return webpage_regex.findall(html)
            
def get_id(html):
    webpage_regex=re.compile("""<dd[^>]+id=["'](.*?)["']""",re.IGNORECASE)
    m= webpage_regex.findall(html)
    for n in m:
        if re.match('htmltxt_',n):
            return n
        
def write(filename,title,chaodai,author,tag1,shi):
    with open('/gushiwen/'+filename+'.txt','w',encoding='utf8')as f:
        f.write(title+'\n')
        f.write(chaodai+'\n')
        f.write(author+'\n')
        f.write('标签：')
        for i in tag1:
            if i!='':
                f.write(str(i))
        f.write('\n')
        f.write(shi)
        
def crawl(url,link_regex):
    for i in range(0,3):
        if i==0:
            html0=download(url)
        else:
            html0=download(url+'0/0/0/0/0/'+str(i)+'/')
        for link in get_links(html0):
            if re.match(link_regex,link):
                abs_link=urljoin(url,link)
                if abs_link  not in links:
                     html=download(abs_link)
                     soup=BeautifulSoup(html,'lxml')
                     _id_=get_id(html)
                     shi=soup.select('dd#'+_id_).pop().text
                     title=soup.find('h2').text
                     tag=soup.select('div.fxbox_video').pop().text
                     s=soup.find('div', {'class':"f-l"}).text
                     chaodai=s.split('\xa0')[-1]
                     author=s.split('\xa0')[0]
                     tag1=tag.split("\n")
                     write(_id_,title,chaodai,author,tag1,shi)
                     links.append(abs_link)
if __name__=='__main__':
    url='https://www.xzslx.net/gushi/'
    link_regex='/shi/'
    create()
    crawl(url,link_regex)            
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        