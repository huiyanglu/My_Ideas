#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
# Date: 2019-08-27

from aiyo_2 import request
from bs4 import BeautifulSoup
import pymysql.cursors
import re
import time

def main(url):
    rst = request.get(url,3) #回调函数
    max_num = BeautifulSoup(rst.text, 'lxml').find('div', {'class': 'paginator'}).find_all('a')[-2].get_text()
    bashurl = 'https://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start='
    for num in range(0,int(max_num)+1):
        url = bashurl + str(num*20) + '&type=T.html'
        each_page(num,url)
    return "全部爬取完毕！！"


def each_page(num,url):
    rst2 = request.get(url, 3)  # 回调函数
    rst2.encoding = 'utf-8'
    tds = BeautifulSoup(rst2.text, 'lxml').find('ul', {'class': 'subject-list'}).find_all('li')
    for td in tds:
        item = each_book(td)
        save_data(item)
    return "第"+str(num)+"页已全部保存~~~"

def each_book(td):
    num2 = 1
    item = {}
    num2+=1
    novelname = td.find('div', {'class': 'info'}).find('a').get_text()
    novelname2 = "".join(novelname.split())
    novelname3 = novelname2.replace('\'','\"')
    novelurl = td.find('a')['href']
    item['name'] = str(novelname3)
    item['name_url'] = novelurl
    name_id = str(novelurl)[-8:-1]
    item['name_id'] = name_id
    author = td.find('div',{'class':'pub'}).get_text().split('/')[0]
    author2 = "".join(author.split())
    item['author'] = author2
    about_rate = td.find('div',{'class':'star clearfix'})
    rate = 0
    if about_rate.find('span', {'class': 'rating_nums'}):
        rated_num = about_rate.find('span',{'class':'pl'}).get_text()
        rated_num2 = re.findall(r'\d+',rated_num)[0]
        rate = about_rate.find('span',{'class':'rating_nums'}).get_text()
    else:
        rated_num2 = 0
    item['rated_num'] = rated_num2
    if not rate:
        rate = 0
    item['rate'] = rate
    return item

def save_data(item):
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='87869973lhy',
        db='douban_bk',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    sql = "INSERT INTO internet_bk VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
    data = (str(item['name']),str(item['author']),str(item['name_id']),str(item['name_url']),str(item['rated_num']),str(item['rate']))
    print(data)
    cursor.execute(sql % data)
    connect.commit()

    print('成功插入数据')

start = time.perf_counter() # 程序运行起始时间
main('https://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start=0&type=T')
end = time.perf_counter()  # 记录程序结束时间
print('保存结束，花费时间：%f s' % (end - start))