#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time : 2019/2/13 上午10:38 
# @Author : zhubc 
# @File : CommonUse.py 
# @Software: PyCharm


import os, sys, time
pack_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pack_dir)
from client import *
from datetime import datetime

data_dir = os.path.join(pack_dir, 'images/image_insert/')


class DeletePeraon(unittest.TestCase):
    '''delete_person接口测试'''

    @classmethod
    def setUpClass(cls):
        cls.__url = r'http://127.0.0.1:19641/search/image/delete_person'
        cls.__now = time.strftime("%Y-%m-%d %H_%M_%S")
        cls.__path = pack_dir + '/result/' + cls.__now + '_result.csv'
        cls.expired_data = {'api_id': '123',
                            'api_secret': '123'}
        cls.no_permission_data = {'api_id': '123',
                                  'api_secret': '123'}
        cls.quota_data = {'api_id': '123',
                          'api_secret': '123'}

        print("初始化数据完成。")

    @classmethod
    def tearDownClass(cls):
        print()
        print("All cases finished.")

    def setUp(self):
        self.client = Client(url=self.__url, method=Method.POST, type=Type.FORM_FILE)
        self.__data = {"api_id": "123", "api_secret": "123"}
        self.__file = {"file": open(data_dir + '/normal.jpg', 'rb')}
        self.start = datetime.now()
        print(self.start)
        print('##############test start###############')

    def tearDown(self):
        self.end = datetime.now()
        print((self.end - self.start).seconds)
        print('##############test end###############')

    def test_01apiid_wrong(self):
        '''api_id错误，UNAUTHORIZED，401'''
        self.__data['api_id'] = '123'
        client = self.client
        client.set_data(self.__data)
        client.set_files(self.__file)
        client.send()
        client.write_to_csv(self.__path)
        client.check_status_code(401)
        client.check_dict_equal({'request_id': 'request_id', 'status': 'UNAUTHORIZED'})

    def test_02apiid_null(self):
        '''api_id为空，UNAUTHORIZED，401'''
        self.__data['api_id'] = ''
        client = self.client
        client.set_data(self.__data)
        client.set_files(self.__file)
        client.send()
        client.write_to_csv(self.__path)
        client.check_status_code(401)
        client.check_dict_equal({'request_id': 'request_id', 'status': 'UNAUTHORIZED'})

    def test_03apiid_miss(self):
        '''缺少api_id，UNAUTHORIZED，401'''
        self.__data.pop('api_id')
        client = self.client
        client.set_data(self.__data)
        client.set_files(self.__file)
        client.send()
        client.write_to_csv(self.__path)
        client.check_status_code(401)
        client.check_dict_equal({'request_id': 'request_id', 'status': 'UNAUTHORIZED'})

    def test_04normal(self):
        """传两张含两张人脸的图"""
        client = self.client
        client.set_files(self.__file)
        client.set_data(self.__data)
        client.send()
        client.transmit('image_id', '$.image_one.image_one_id')
        client.write_to_csv(self.__path)
        client.check_status_code(200)
        client.check_dict_equal(
            {"request_id": "request_id", "status": "OK",
             "confidences": [[1.0, 0.902], [0.902, 1.0]], "max_confidence": 1.0,
             "image_one": {"image_one_id": "image_one_id"},
             "image_two": {"image_two_id": "image_two_id"}})

    def test_05normal_image_id(self):
        """传正常的image_id和image_two_id"""
        client = self.client
        self.__data['image_one_id'] = client.value('image_id')
        client.set_data(self.__data)
        client.send()
        client.write_to_csv(self.__path)
        client.check_status_code(200)
        client.check_dict_equal({"request_id": "request_id", "status": "OK",
                                 "confidences": [[1.0, 0.902], [0.902, 1.0]], "max_confidence": 1.0})
