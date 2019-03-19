#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time : 2019/3/13 上午9:51 
# @Author : zhubc 
# @File : tcpclient.py 
# @Software: PyCharm
import json
import socket
import unittest
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class TcpClient(unittest.TestCase):

    def __init__(self, ip, port, method, max_receive=102400):
        self.__ip = ip
        self.__port = port
        self.__method = method
        self.__max_receive = max_receive
        self.__connected = 0
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__data = {}
        self.__files = {}
        self.__res = None

# =======================Set TCP Request=====================================

    def set_data(self, data):
        if isinstance(data, dict):
            self.__data = json.dumps(data).encode()
        else:
            print('data不是字典类型')

    def set_files(self, files):
        pass

    def connect(self):
        if not self.__connected:
            try:
                self.__sock.connect((self.__ip, self.__port))
            except socket.error as e:
                logging.exception(e)
            else:
                self.__connected = 1
                logging.debug('TCPClient connect to {0}:{1} success.'.format(self.__ip, self.__port))

    def send(self):
        if self.__connected:
            try:
                self.__sock.send(self.__data)
                logging.debug('TCPClient send {0} finish.'.format(self.__data))
            except socket.error as e:
                logging.exception(e)

            try:
                self.__res = self.__sock.recv(self.__max_receive).decode()
                logging.debug('TCPClient received.')
            except socket.error as e:
                logging.exception(e)

    def close(self):
        if self.__connected:
            self.__sock.close()
            logging.debug('TCPClient closed')

# =======================Get TCP Response=====================================

    def res2json(self):
        if self.__res:
            return json.loads(self.__res)
        else:
            print('未获取到响应信息')

# =======================Set TCP Assertion=====================================

    def check_status_code(self, status=200):
        if self.__res.status_code:
            self.assertEqual(self.__res.status_code, status, "检查点失败。\n实际结果{0},\n预期结果{1}".format(self.__res.status_code, status))
            print("检查点成功。\n实际结果{0},\n预期结果{1}".format(self.__res, status))
        else:
            print("未获取到响应状态码")

    def check_dict_equal(self, exp):
        if self.__res:
            self.assertDictEqual(self.res2json(), exp, "检查点失败。\n实际结果{0},\n预期结果{1}".format(self.res2json(), exp))
            print("检查点成功。\n实际结果{0},\n预期结果{1}".format(self.res2json(), exp))
