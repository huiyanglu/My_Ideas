#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu

"""批量重命名指定文件的后缀名"""

import os
import argparse

def batch_rename(work_dir, old_ext, new_ext):
    files = os.listdir(work_dir)
    print(os.listdir(work_dir))
    print("Start!")
    for filename in files:
        portion = os.path.splitext(filename) #文件名以点为分割点被分开
        file_ext = portion[1]
        if old_ext == file_ext:
            new_file_ext = portion[0]+new_ext
            os.rename(os.path.join(work_dir,filename),os.path.join(work_dir,new_file_ext))
    print('Rename is done!')
    print(os.listdir(work_dir))

def get_parser():
    parser = argparse.ArgumentParser(description='change extension of files in a working directory')
    parser.add_argument('work_dir', metavar='WORK_DIR', type=str, nargs=1,
                        help='the directory where to change extension')
    parser.add_argument('old_ext', metavar='OLD_EXT', type=str, nargs=1, help='old extension')
    parser.add_argument('new_ext', metavar='NEW_EXT', type=str, nargs=1, help='new extension')
    return parser

def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    work_dir = args['work_dir'][0]
    old_ext = args['old_ext'][0]
    if old_ext[0] != '.':
        old_ext = '.' + old_ext
    new_ext = args['new_ext'][0]
    if new_ext[0] != '.':
        new_ext = '.' + new_ext
    batch_rename(work_dir,old_ext,new_ext)

if __name__ == '__main__':
    main()

"""
测试：terminal输入，位置切换至Python文件所在位置
python3 batch_file_rename.py ./test_1 .txt .txt2
参考自：https://github.com/geekcomputers/Python/blob/master/batch_file_rename.py
"""