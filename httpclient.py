#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time : 2019/3/12 下午4:04 
# @Author : zhubc 
# @File : httpclient.py 
# @Software: PyCharm
import csv
import pandas
import unittest

import jsonpath
import requests


class Method:
    POST = 'POST'
    GET = 'GET'


class Type:
    FORM_data = 0
    URL_ENCODE = 1
    JSON = 2
    XML = 3
    FORM_FILE = 4
    FILE = 5


class HttpClient(unittest.TestCase):

    VALUES = {}

    def __init__(self, url, method, type=0):
        self.__url = url
        self.__method = method
        self.__type = type
        self.__headers = {}
        self.__files = {}
        self.__data = {}
        self.__res = None

# =======================Set Http Request=============================

    def set_headers(self, headers):
        if isinstance(headers, dict):
            self.__headers = headers
        else:
            raise Exception('headers为字典类型')

    def set_files(self, files):
        if isinstance(files, dict):
            self.__files = files
        else:
            raise Exception('files为字典类型')

    def set_data(self, data):
        if isinstance(data, dict):
            if self.__type == 0 or self.__type == 4 or self.__type == 5:
                self.__headers['Content-Type'] = 'multipart/form-data'
            elif self.__type == 1:
                self.__headers['Content-Type'] = 'application/x-www-form-urlencoded'
            elif self.__type == 2:
                self.__headers['Content-Type'] = 'application/json'
            elif self.__type == 3:
                self.__headers['Content-Type'] = 'text/xml'
            else:
                raise Exception('请求正文类型不支持')
            self.__data = data
        else:
            raise Exception('正文数据类型为字典')

    def send(self):
        if self.__method == 'GET':
            self.__res = requests.get(url=self.__url, headers=self.__headers, params=self.__data)
        elif self.__method == 'POST':
            if self.__type == 0:
                self.__res = requests.post(url=self.__url, headers=self.__headers, data=self.__data)
            elif self.__type == 4:
                self.__res = requests.post(url=self.__url, headers=self.__headers, data=self.__data, files=self.__files)
            elif self.__type == 5:
                self.__res = requests.post(url=self.__url, headers=self.__headers, files=self.__files)
            elif self.__type == 1:
                self.__res = requests.post(url=self.__url, headers=self.__headers, data=self.__data)
            elif self.__res == 2:
                self.__res = requests.post(url=self.__url, headers=self.__headers, json=self.__data)
            elif self.__type == 3:
                xml_str = self.__data.get('xml')
                if xml_str and isinstance(xml_str, str):
                    self.__res = requests.post(url=self.__url, data=xml_str, headers=self.__headers, verify=False)
                else:
                    raise Exception('xml正文的请求，请正确添加xml字符串')
        else:
            raise Exception('不支持的请求方法类型')

# =======================Get Http Response=============================

    @property
    def url(self):
        return self.__url

    @property
    def method(self):
        return self.__method

    @property
    def type(self):
        return self.__type

    @property
    def text(self):
        if self.__res.status_code:
            return self.__res.text
        else:
            return None

    @property
    def status_code(self):
        if self.__res.status_code:
            return self.__res.status_code
        else:
            return None

    @property
    def response_time(self):
        if self.__res.status_code:
            return round(self.__res.elapsed.total_seconds() * 1000)
        else:
            return None

    @property
    def res_headers(self):
        if self.__res.status_code:
            return self.__res.headers
        else:
            return None

    def res_to_json(self):
        if self.__res.status_code:
            try:
                return self.__res.json()
            except Exception:
                return None
        else:
            return None

# =======================Set Http Assertion=============================

    def check_status_code(self, status=200):
        if self.__res.status_code:
            self.assertEqual(self.__res.status_code, status,
                             "响应状态码错误：实际结果[{first}]，预期结果[{second}]".format(first=self.__res.status_code), second=status)
            print("检查点成功。实际结果[{first}]，预期结果[{second}]".format(first=self.__res.status_code, second=status))
        else:
            self.assertTrue(False, "无法获取相应状态码:" + str(self.__res.text))

    def check_equal(self, first, second, msg=None):
        self.assertEqual(first, second, msg)

    def check_not_equal(self, first, second, msg=None):
        self.assertNotEqual(first, second, msg)

    def check_jsonNode_equal(self, path, exp, msg=None):
        if self.__res.json():
            node = self.json_value(path)
            self.assertEqual(node, exp, msg)
            print("检查点成功，实际结果[{first}]，预期结果[{second}]".format(first=node, second=exp))

    def check_dict_equal(self, exp):
        if self.__res.json():
            res = self.__res.json()
            if res.get('request_id') and res.get('image_id') and res.get('person_uuid'):
                res['request_id'] = 'request_id'
                res['image_id'] = 'image_id'
                res['person_uuid'] = 'person_uuid'
            elif res.get('request_id') and res.get('image_one') and res.get('image_two'):
                res['request_id'] = 'request_id'
                res['image_one']['image_one_id'] = 'image_one_id'
                res['image_two']['image_two_id'] = 'image_two_id'
            elif res.get('request_id') and res.get('image_one'):
                res['request_id'] = 'request_id'
                res['image_one']['image_one_id'] = 'image_one_id'
            elif res.get('request_id') and res.get('image_two'):
                res['request_id'] = 'request_id'
                res['image_two']['image_two_id'] = 'image_two_id'
            elif res.get('request_id') and res.get('image_id') and res.get('liveness_data_id'):
                res['request_id'] = 'request_id'
                res['image_id'] = 'image_id'
                res['liveness_data_id'] = 'liveness_data_id'
            elif res.get('request_id') and res.get('image_id') and res.get('time_used'):
                res['request_id'] = 'request_id'
                res['time_used'] = 'time_used'
                res['image_id'] = 'image_id'
            elif res.get('request_id') and res.get('image_id'):
                res['request_id'] = 'request_id'
                res['image_id'] = 'image_id'
            elif res.get('request_id') and res.get('liveness_data_id'):
                res['request_id'] = 'request_id'
                res['liveness_data_id'] = 'liveness_data_id'
            elif res.get('request_id') and res.get('feature_image_id'):
                res['request_id'] = 'request_id'
                res['feature_image_id'] = 'feature_image_id'
            else:
                res['request_id'] = 'request_id'

            if res.get('hack_score') and res.get('verify_score'):
                res['hack_score'] = self.round_float(res.get('hack_score'), 3)
                res['verify_score'] = self.round_float(res.get('verify_score'), 3)
            elif res.get('hack_score'):
                res['hack_score'] = self.round_float(res.get('hack_score'), 3)
            elif res.get('verify_score'):
                res['verify_score'] = self.round_float(res.get('verify_score'), 3)
            elif res.get('confidences') and res.get('max_confidence'):
                res['max_confidence'] = self.round_float(res.get('max_confidence'), 3)
                for scores in res.get('confidences'):
                    for i in range(0, len(scores)):
                        scores[i] = self.round_float(scores[i], 3)
            else:
                pass
            self.assertDictEqual(res, exp, "返回json不匹配:\n实际结果:[{first}]\n预期结果:[{second}]".format(first=res, second=exp))
            print('检查点成功。')
            print('实际结果：{first}'.format(first=res))
            print('预期结果：{second}'.format(second=exp))

    # =======================Some Useful Tools=============================

    def json_value(self, path):
        if self.__res.json():
            obj = jsonpath.jsonpath(self.__res.json(), path)
            if obj:
                return obj[0]
        else:
            return None

    def json_values(self, path):
        if self.__res.json():
            obj = jsonpath.jsonpath(self.__res.json(), path)
            if obj:
                return obj
        else:
            return None

    def transmit(self, name, path):
        """存储测试用例中需要向后传递的值"""
        node = self.json_value(path)
        if node:
            HttpClient.VALUES[name] = node
        else:
            raise Exception("未获取到要传递的值：" + path)

    def value(self, name):
        """获取已经存储的值"""
        value = HttpClient.VALUES.get(name)
        if value:
            return value
        else:
            raise Exception("要获取的变量不存在：" + name)

    def write_headers(self, path):
        headers = ['status', 'url', 'apiid', 'file', 'data', 'response']
        try:
            with open(path, mode='a', encoding='utf-8', errors='ignore') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(headers)
        except Exception as e:
            print(e)
            raise Exception('存储路径错误')

    def write_to_csv(self, path):
        try:
            with open(path, mode='a', encoding='utf-8', errors='ignore') as f:
                csv_write = csv.writer(f)
                csv_write.writerow([self.status_code, self.__url, self.__data.get('api_id'), self.__files, self.__data,
                                    self.res_to_json()])
        except Exception as e:
            print(e)
            raise Exception("存储路径错误")

    def data_statistics(self, path):
        df = pandas.read_csv(path)
        return df[df.apiid == '557c656d71f54a7e8f8c681d7a9ab006'].status.value_counts()

    # 截取n位小数，不四舍五入
    def round_float(self, num, n):
        if isinstance(num, float):
            a, b = str(num).split('.')
            b = b[:n]
            return float('.'.join([a, b]))
        elif isinstance(num, str):
            try:
                a, b = num.split('.')
                b = b[:n]
                return '.'.join([a, b])
            except Exception:
                print("num字符串内容不是小数")
        elif num == 0 or num == '0':
            return num
        else:
            print("num参数不是小数")
