#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

from PIL import Image
import os
import re

def connect_imgs():
    # 从当前路径进入文件夹，获取所有文件夹名，存入字典
    path=r'connect_test' #文件夹名
    name_dict = {} #所有需要处理的文件夹合集字典
    for each_filename in os.listdir(path): #由当前路径进入path文件夹
        if each_filename[0].isdigit(): #判断是否为想要的文件夹
            file_num = re.findall(r'(\d+)-',each_filename)[-1]
            name_dict[file_num] = each_filename

    # 获取每个文件夹中需要处理的文件
    for i in range(1,len(name_dict)+1):
        each_path = os.getcwd()+'/'+path+'/'+name_dict[str(i)] #获取目标文件夹的路径
        each_name = os.listdir(each_path) # 获取当前文件夹中的文件名称列表
        print(each_name)

        # 筛选需要处理的文件
        name_list = []
        each_name_5 = [each[:-5] for each in each_name]
        for x in range(len(each_name_5)-1):
            for y in range(x+1,len(each_name_5)):
                if each_name_5[x]==each_name_5[y]:
                    name_list.append(each_name[x])
                    name_list.append(each_name[y])
                    break
            if name_list:break # 退出多重循环

        # 如果存在需要处理的文件
        if name_list:
            connection(each_path,name_list) #调用函数，拼图

    return '拼图完毕！'

def connection(each_path,name_list):
    # 读取待处理文件list中所有JPG图像（注意后缀可能是.jpg或.JPG）
    # 注意路径选择
    im_list = [Image.open(each_path+'/'+fn) for fn in name_list if (fn.endswith('.jpg') or fn.endswith('.JPG'))]

    # 图片转化为相同的尺寸
    imgs = []
    for i in im_list:
        # 图片size分类
        if i.size[0]>i.size[1]:
            new_img = i.resize((2606, 1879), Image.BILINEAR)
        else:
            new_img = i.resize((2033, 2874), Image.BILINEAR)
        imgs.append(new_img)

    # 单幅图像尺寸
    width, height = imgs[0].size

    # 创建空白长图
    result = Image.new(imgs[0].mode, (width, height * len(imgs)))

    # 拼接图片
    for i, im in enumerate(imgs):
        result.paste(im, box=(0, i * height))

    # 保存图片
    result.save(each_path+'/'+name_list[0][:-4] + '合并.jpg')

    # 删除旧图
    os.remove(each_path+'/'+name_list[0])
    os.remove(each_path+'/'+name_list[1])

if __name__ == '__main__':
    connect_imgs()
