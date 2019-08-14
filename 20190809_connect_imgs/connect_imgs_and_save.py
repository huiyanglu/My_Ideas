#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

from PIL import Image
import os
import re

# 定位所有需要拼图的图片
def connect_imgs():
    # 从当前路径进入文件夹，获取所有文件夹名，存入字典
    path=r'connect_zhengshu' #文件夹名
    name_dict = target_file(path)

    # 获取每个文件夹中需要处理的文件
    for i in name_dict:
        final_path = name_dict[i]
        each_path = os.getcwd()+'/'+path+'/'+final_path #获取目标文件夹的路径
        each_name = os.listdir(each_path) # 获取当前文件夹中的文件名称列表
        print(each_name)

        # 筛选需要处理的文件
        name_list = {}
        each_name_5 = [each[-4:] for each in each_name]
        for each in range(len(each_name_5)):
            if each_name_5[each]=='.jpg' or each_name_5[each]=='.JPG':
                name_list_num = re.findall(r'(\d+).',each_name[each])[-1]
                name_list[name_list_num]=each_name[each]
        print(name_list)

        # 根据key的升序排列，把key value都打印出来
        new_sys1 = sorted(name_list.items(), key=lambda d: d[-1], reverse=False)
        name_list2 = [new_sys1[i][1] for i in range(len(new_sys1))]
        # 如果存在需要处理的文件
        if name_list2:
            connection(each_path,name_list2) #调用函数，拼图

    return '拼图完毕！'


# 拼接图片
def connection(each_path,name_list):
    # 读取待处理文件list中所有JPG图像（注意后缀可能是.jpg或.JPG）
    # 注意路径选择
    im_list = [Image.open(each_path+'/'+fn) for fn in name_list if (fn.endswith('.jpg') or fn.endswith('.JPG'))]

    # 图片转化为相同的尺寸
    imgs = []
    max = 0
    heng=0
    shu=0
    for i in im_list:
        # 图片size分类
        if i.size[0]>i.size[1]:
            new_img = i.resize((2606, 1879), Image.BILINEAR)
            heng+=1
            if max<2606:max=2606
        else:
            new_img = i.resize((1329, 1879), Image.BILINEAR)
            shu+=1
            if max<1329:max=1329
        imgs.append(new_img)
    print(imgs)
    # 单幅图像尺寸
    if heng:
        width, height = (2606, 1879)
    else:
        width, height = (1329, 1879)

    # 创建空白长图
    result = Image.new(imgs[0].mode, (max, 1879*len(imgs)))

    # 拼接图片
    for i, im in enumerate(imgs):
        result.paste(im, box=(0, i * height))

    # 保存图片
    result.save(each_path+'/'+name_list[0][:-4] + '合并.jpg')

    # 删除旧图
    # os.remove(each_path+'/'+name_list[0])

# 将拼好的图片存入目标文件夹
def replace_imgs():
    # 从当前路径进入文件夹，获取所有文件夹名，存入字典
    path=r'connect_test' #文件夹名
    file_path = r'connect_zhengshu'
    rst_name_dict = target_file(path)
    name_dict = saved_file(file_path)

    for i in rst_name_dict:
        final_path = rst_name_dict[i]
        rst_each_path = os.getcwd() + '/' + path + '/' + final_path  # 获取目标文件夹的路径

        if i in name_dict:
            final_path2 = name_dict[i]
            each_path2 = os.getcwd() + '/' + file_path + '/' + final_path2  # 获取目标文件夹的路径
            each_name = os.listdir(each_path2)  # 获取当前文件夹中的文件名称列表

            # 打开权证图片
            img_path = name_dict[i]
            img_path2 = os.getcwd() + '/' + file_path + '/' + img_path
            rst_img = [Image.open(img_path2 + '/' + fn) for fn in each_name if (fn.endswith('合并.jpg'))]

            # 保存图片到目标路径
            rst_img[0].save(rst_each_path+'/'+final_path2+'.jpg')
    return 'ok'

#存放图片的目标文件夹中的所有文件名
def target_file(path):
    rst_name_dict = {}  # 所有需要处理的文件夹合集字典
    for each_filename in os.listdir(path):  # 由当前路径进入path文件夹
        if each_filename[0].isdigit():  # 判断是否为想要的文件夹
            file_num = re.findall(r'第(\d+)号-', each_filename)[-1]
            rst_name_dict[file_num] = each_filename
    return rst_name_dict

#准备读取照片的文件夹中的所有文件名
def saved_file(path):
    name_dict = {}  # 所有需要处理的文件夹合集字典
    for each in os.listdir(path):  # 由当前路径进入path文件夹
        if each[0] == '江':  # 判断是否为想要的文件夹
            file_num = re.findall(r'第(\d+)号—', each)[-1]
            name_dict[file_num] = each
    return name_dict

#print(connect_imgs())
print(replace_imgs())