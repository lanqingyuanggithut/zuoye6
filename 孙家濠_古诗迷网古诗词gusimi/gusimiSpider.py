from bs4 import BeautifulSoup as bs
import requests
import os
def get(web,foldname,num):
    for i in range(num):                               
        page=requests.get(web%(i))
        if page.status_code==200:#我这里用的是老师上课讲的  网页无报错就进行爬取            
            soup=bs(page.content, 'lxml')
            if not os.path.exists(foldname):
                os.makedirs(foldname) 
            title=soup.select('.box_title h2')[0].text
            dynasty=soup.select('.old_h1 a')[0].text
            autor=soup.select('.old_h1 a')[1].text               
            tags=[]#我在处理标签加逗号废了好大劲。。有什么更简便的方法求指导
            for n in range(len(soup.select('.newstext a'))):
                tag=soup.select('.newstext a')[n].text
                tags.append(tag)          
            taglist=str(tags)[1:-1].replace('\'','')
            content=soup.select('.newstext')[0].text 
            with open(foldname+'/%d.txt'%i,'w',encoding='utf8') as f:
                    f.write('title:'+title+'\n')
                    f.write('dynasty:'+dynasty+'\n')
                    f.write('autor:'+autor+'\n')                    
                    f.write('content:'+content+'\n')
                    if len(soup.select('.newstext')[1]) !=1:#判断一下标签是否存在
                        f.write('tag:'+taglist+'\n')            
if __name__=='__main__':
    get('https://www.gushimi.org/gushi/%d.html','www.gushimi.org/',50)