#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

"""
Project: Python爬虫--selenium和request结合爬取SooPAT专利信息
Date: 2019-08-24
Author: huiyanglu
Content:
本项目用于根据专利号爬取对应专利的具体信息，包括专利名称、发明人、申请时间、公开时间、是否有权等。
由于SooPAT网址需要登录和验证，本项目采用selenium模拟登录，手动点击验证的形式。
爬取的数据保存到MySQL中。

"""
import numpy as np
from aiyo_2 import request
from bs4 import BeautifulSoup
import pymysql.cursors
import time
from selenium import webdriver

# txt数据读取
data = np.loadtxt('patent_info.txt', delimiter='\n')
patent_num = [str(int(i)) for i in data]

def login(url):
    driver = webdriver.Chrome()
    username = '******'
    password = '******'

    # 打开登陆网页
    driver.get(url)
    time.sleep(5)

    # 模拟登陆
    driver.find_element_by_xpath(
        "./html/body/div[2]/div[2]/div[1]/form/table/tbody/tr[1]/td[2]/input[1]"). \
        send_keys(username)
    driver.find_element_by_xpath(
        "./html/body/div[2]/div[2]/div[1]/form/table/tbody/tr[2]/td[2]/input"). \
        send_keys(password)
    driver.find_element_by_xpath(
        "./html/body/div[2]/div[2]/div[1]/form/table/tbody/tr[4]/td[2]/input").click()
    time.sleep(3)

    # 滑块待修改
    # button = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]')
    # action = ActionChains(driver)
    # action.click_and_hold(button).perform()
    # action.reset_actions()
    # action.move_by_offset(180, 0).perform()

    #driver.refresh()

    # 模拟登陆完成，输入搜索内容
    # driver.find_element_by_xpath(".//*[@id='SearchWord']").send_keys(word)  # 输入搜索内容
    # driver.find_element_by_xpath("./html/body/center/table/tbody/tr[1]/td[3]/button").click()  # 点击搜索
    # time.sleep(10)
    # driver.implicitly_wait(10)
    # driver.get('http://www.soopat.com/Patent/'+word)
    # time.sleep(10)

# 手动点击验证
def test(url):
    driver = webdriver.Chrome()
    driver.get(url)
    rst = request.get(url, 3)
    x = BeautifulSoup(rst.text, 'lxml')
    if '申请号' not in x:
        time.sleep(10)
    else:
        time.sleep(2)

def patent_info():
    login('http://t.soopat.com/index.php?mod=login&return_url=http%3A//www.soopat.com/Home/Index')

    for each_patent in patent_num:
        patent_dict = {}
        patent_url = 'http://www.soopat.com/Patent/' + each_patent
        test(patent_url)
        rst = request.get(patent_url, 3)
        x = BeautifulSoup(rst.text, 'lxml')
        title = BeautifulSoup(rst.text, 'lxml').find('span', {'class': 'detailtitle'}).get_text()
        if '有权' in title:
            title2 = title.split('有权')[0]
            valid = '有权'
        elif '无权' in title:
            title2 = title.split('无权')[0]
            valid = '无权'
        patent_dict['valid'] = valid
        title3 = "".join(title2.split())
        patent_dict['title'] = title3
        patent = title.split('申请号：')[-1].split('申请日')[0]
        patent_dict['patent_number'] = patent
        apply_date = title.split('申请日：')[-1]
        apply_date2 = "".join(apply_date.split())
        patent_dict['apply_date'] = apply_date2
        applicant = BeautifulSoup(rst.text, 'lxml').find('div', {'class': 'detailinfo'}).find_all('td')[-4]
        applicant2 = applicant.get_text().split('：')[1:]
        applicant3 = ','.join(applicant2[0].split(' '))
        patent_dict['applicants'] = applicant3[1:]
        auth_date = BeautifulSoup(rst.text, 'lxml').find_all('div', {'class': 'vipcom'})[1].get_text()
        auth_date2 = auth_date.split('公开日')[1].split('专利代理机构')[0]
        auth_date3 = ''.join(auth_date2.split())
        patent_dict['auth_date'] = auth_date3
        print(patent_dict)

        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='***',
            db='***',
            charset='utf8'
        )
        # 获取游标
        cursor = connect.cursor()
        sql = "INSERT INTO *** VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
        data = (str(title3), str(valid), str(patent), str(apply_date2), str(applicant3[1:]), str(auth_date3))
        print(data)
        cursor.execute(sql % data)
        connect.commit()

        print('成功插入数据')

patent_info()