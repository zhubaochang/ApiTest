#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time : 2019/3/20 上午9:36 
# @Author : zhubc 
# @File : run.py.py 
# @Software: PyCharm
import re
import os
import smtplib
import time
import unittest
from email.header import Header
from email.mime.text import MIMEText
from httpclient import *

import HTMLTestReportCN
from util import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_value(dic, name):
    source = dic.get(name)
    if source is None or source == '':
        return None
    else:
        variable_regexp = r"\$([\w_]+)"
        result = re.findall(variable_regexp, source)
        if len(result) > 0:
            value = DATA.get(result[0])
            if value:
                source = source.replace('$'+result[0], value)
            else:
                return None
        return source


# ======================查找最新测试报告============================
def new_report(filepath):
    filelist = os.listdir(filepath)
    filesort = sorted(filelist, key=lambda x: os.path.getmtime(filepath + x))
    filenew = os.path.join(filepath, filesort[-1])
    return filenew


# ======================发送测试报告================================
def send_report(reportfile):
    with open(reportfile, 'rb') as f:
        mail_body = f.read()
        mail_config = util.read_jsonfile(os.path.join(BASE_DIR, 'config.json'))
        msg_from = mail_config['email'].get('from')   # 发件箱
        passwd = mail_config['email'].get('to')       # 授权码
        msg_to = mail_config['email'].get('passwd')   # 收件箱
        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg['From'] = msg_from
        msg['To'] = msg_to
        msg['Subject'] = Header('自动化测试报告', 'utf-8')

        try:
            smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            smtp.login(msg_from, passwd)
            smtp.sendmail(msg_from, msg_to, msg.as_string())
            print('email has send out !')
        except Exception as e:
            print("发送失败：%s" % e)
        finally:
            smtp.quit()


# =========================执行测试用例=====================================
# python脚本案例执行
def run_py_cases(pattern):
    suite = unittest.defaultTestLoader.discover(start_dit=os.path.join(BASE_DIR, '/interface'),
                                                pattern=pattern)

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    report_file = os.path.join(BASE_DIR, '/report', '%s_report.html' % now)
    with open(report_file, 'wb') as f:
        runner = HTMLTestReportCN.HTMLTestRunner(stream=f,
                                                 title='接口自动化测试报告',
                                                 description="""
                                    运行环境:Python3, Requests, unittest;\n
                                    java测试环境地址:http://127.0.0.1:19641;\n
                                    ruby测试环境地址:http://127.0.0.2:10006
                                    """)
        runner.run(suite)


# excel案例执行
def run_excel_cases():
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    result_path = BASE_DIR + '/result/' + now + '_result.csv'
    case_path = BASE_DIR + '/excel_cases/%s.xlsx' % read_runconfig(BASE_DIR+'/config.xml', 'excelcases')[0]
    cases = util.read_config_excel(case_path, '用例').get('用例')
    if cases:
        suite = unittest.TestSuite()
        for case in cases:
            id = get_value(case, '用例编号')
            des = get_value(case, '用例描述')
            url = get_value(case, '地址')
            method = get_value(case, '方法类型')
            type = get_value(case, '参数类型')
            headers = get_value(case, '请求头')
            files = get_value(case, '文件参数')
            data = get_value(case, '参数')
            checks = get_value(case, '检查点')
            if not headers:
                headers = {}
            if not files:
                files = {}
            if not data:
                data = {}
            if checks:
                checks = checks.split('&')
            FUNC_TEMPLATE = """class {classes}(unittest.TestCase):
    def test_{id}(self):
        '''{des}'''
        url = '{url}'
        method = Method.{method}
        type = Type.{type}
        headers = {headers}
        files = {files}
        data = {data}
        path = '{path}'
        client = Client(url=url, method=method, type=type)
        client.set_headers(headers)
        client.set_files(files)
        client.set_data(data)
        client.send()
        client.write_to_csv(path)\n"""
            func = FUNC_TEMPLATE.format(classes=id.upper(), id=id, des=des, url=url, method=method, type=type,
                                        headers=headers, files=files, data=data, path=result_path)
            for check in checks:
                func += '        client.%s\n' % check
            exec(func)
            ADD = 'suite.addTest({case}("test_{method}"))'
            exec(ADD.format(case=id.upper(), method=id))
        title = '%s.html' % now
        fp = open(os.path.join(BASE_DIR, 'report', title), 'wb')
        HTMLTestReportCN.HTMLTestRunner(stream=fp, title='接口测试报告').run(suite)
        fp.close()


if __name__ == '__main__':
    run_py_cases('test*.py')

