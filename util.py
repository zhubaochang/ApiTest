#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time : 2019/3/20 上午10:47 
# @Author : zhubc 
# @File : util.py 
# @Software: PyCharm
import json
import os
from xml.etree import ElementTree as ET
import xlrd


def read_jsonfile(path):
    if os.path.exists(path):
        with open(path) as f:
            config = json.loads(f.read())
            return config
    else:
        raise Exception("配置文件不存在")


def read_config(filepath, nodepath):
    try:
        et = ET.parse(filepath)
    except FileNotFoundError:
        raise Exception('项目配置文件不存在:'+filepath)
    else:
        datas = et.findall(nodepath)
        if len(datas) > 0:
            re = {}
            for data in datas:
                re[data.tag] = data.text
            return re
        else:
            raise Exception('未找到配置信息')


def read_runconfig(filepath, nodepath):
    try:
        et = ET.parse(filepath)
    except FileNotFoundError:
        raise Exception('项目配置文件不存在:'+filepath)
    else:
        cases = et.findall('.//%s/*' % nodepath)
        if len(cases) > 0:
            list = []
            for case in cases:
                list.append(case.tag)
            return list
        else:
            raise Exception('在配置文件中未找到可执行的用例信息')


def read_config_excel(filepath, sheet_name):
    try:
        book = xlrd.open_workbook(filepath)
        table = book.sheet_by_name(sheet_name)
    except Exception:
        raise Exception('项目配置文件不存在:'+filepath+' '+sheet_name)
    else:
        nrows = table.nrows
        if nrows > 0:
            li = []
            for n in range(1, nrows):
                values = table.row_values(n)
                data = {}
                for i in range(0, len(values)):
                    ctype = table.cell_type(n, i)
                    if ctype == 2 and values[i] % 1 == 0:
                        data[table.cell_value(0, i)] = str(int(values[i]))
                    elif ctype == 2 and values[i] % 1 != 0:
                        data[table.cell_value(0, i)] = str(values[i])
                    elif ctype == 3:
                        date = xlrd.xldate_as_datetime(values[i], 0)
                        data[table.cell_value(0, i)] = date.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        data[table.cell_value(0, i)] = values[i]
                else:
                    li.append(data)
            return {sheet_name: li}
        else:
            raise Exception('配置文件为空')


if __name__ == '__main__':
    read_jsonfile('./config.json')
